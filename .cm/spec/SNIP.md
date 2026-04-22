# Code snippets for the descriptor rework

Companion to `PLAN.md`. Every snippet has a heading anchor; the plan
references them by those anchors rather than inlining. Line references into
the existing codebase point at the current tree as of this rework's
starting point.

---

## Snip 01 — `ss_whitelist.h` interface

```c
typedef enum {
  SS_SCRIPT_P2PKH = 0,     // BIP44, purpose 44
  SS_SCRIPT_P2SH_P2WPKH,   // BIP49, purpose 49
  SS_SCRIPT_P2WPKH,        // BIP84, purpose 84
  SS_SCRIPT_P2TR,          // BIP86, purpose 86 (single-key)
} ss_script_type_t;

typedef struct {
  ss_script_type_t script;
  uint32_t purpose;        // 44/49/84/86 (unhardened)
  uint32_t coin;           // 0 or 1 (unhardened)
  uint32_t account;        // 0..MAX_ACCOUNT (unhardened)
  uint32_t chain;          // 0 or 1 (unhardened)
  uint32_t index;          // < MAX_INDEX (unhardened)
} ss_keypath_t;

#define SS_MAX_ACCOUNT      100     // matches Ledger
#define SS_MAX_ADDR_INDEX   100     // stricter than Ledger (50000); mirrors account cap

// Generic keypath depth limit (used by the registry matcher, not the
// strict whitelist). 6 origin + 2 trailing = 8 BIP32 components after the
// fingerprint. Mirrors Ledger's registered-wallet cap.
#define MAX_KEYPATH_ORIGIN_DEPTH   6
#define MAX_KEYPATH_TAIL_DEPTH     2
#define MAX_KEYPATH_TOTAL_DEPTH    (MAX_KEYPATH_ORIGIN_DEPTH + MAX_KEYPATH_TAIL_DEPTH)

// Parse a keypath (5 BIP32 components after fingerprint) into ss_keypath_t.
// Returns false if not exactly 5 components or any component violates the
// hardened/unhardened rule for the strict singlesig whitelist shape
// (3 hardened origin + 2 unhardened trailing).
bool ss_keypath_parse(const unsigned char *keypath_after_fp,
                      size_t keypath_len_after_fp,
                      ss_keypath_t *out);

// Returns true if the parsed keypath matches one of the four whitelisted
// script/purpose pairs, the coin type is consistent with `is_testnet`,
// account < SS_MAX_ACCOUNT, index < SS_MAX_ADDR_INDEX.
bool ss_keypath_is_whitelisted(const ss_keypath_t *kp, bool is_testnet);

// Render back to "m/44'/0'/0'/0/5" etc for key_get_derived_key().
int ss_keypath_format(const ss_keypath_t *kp, char *buf, size_t buf_size);

// Derive address / scriptPubKey at (script, account, chain, index).
// Internally calls key_get_derived_key() then script-type specific path.
bool ss_address(ss_script_type_t script, uint32_t account,
                uint32_t chain, uint32_t index, bool is_testnet,
                char **address_out);
bool ss_scriptpubkey(ss_script_type_t script, uint32_t account,
                     uint32_t chain, uint32_t index, bool is_testnet,
                     unsigned char *script_out, size_t *script_len_out);
```

---

## Snip 02 — `registry.h` interface

```c
typedef struct {
  char id[STORAGE_MAX_SANITIZED_ID_LEN + 1];
  storage_location_t loc;        // where it was loaded from
  struct wally_descriptor *desc; // parsed, owned
  int my_key_index;              // key position in the descriptor matching our fp
  uint32_t num_paths;            // 1 or 2 (multipath <0;1>)
  // cached origin-path prefix for our key, e.g. "48'/0'/0'/2'", used
  // to match incoming PSBT keypaths without re-walking the descriptor.
  // Depth up to MAX_KEYPATH_ORIGIN_DEPTH (6) to cover deep registered
  // descriptor origins.
  uint32_t origin_path[MAX_KEYPATH_ORIGIN_DEPTH];
  size_t   origin_path_len;
} registry_entry_t;

// Called after key_load_from_mnemonic() succeeds. Scans flash + SD for .txt
// descriptors, parses each, validates our fingerprint is one of the keys, and
// adds successful ones to the in-memory registry. .kef files are ignored here.
void registry_init(bool is_testnet);

// Current session count / accessor.
size_t registry_count(void);
const registry_entry_t *registry_get(size_t i);
const registry_entry_t *registry_find_by_id(const char *id);

// Find a registry entry whose origin path + our fingerprint match the given
// PSBT keypath. `keypath` starts with the 4-byte fingerprint; total depth
// (origin + trailing) may be up to MAX_KEYPATH_TOTAL_DEPTH (8) BIP32
// components = 32 bytes after the fingerprint. Used by psbt.c. Returns
// NULL if no entry's origin prefix is a match.
const registry_entry_t *registry_match_keypath(const unsigned char *keypath,
                                               size_t keypath_len);

// Add / remove / persist. Used by UI: scanning a new descriptor still goes
// through descriptor_validator; the success path calls registry_add() and
// optionally persists via storage_save_descriptor(..., plaintext). Removal
// also deletes the .txt file.
//
// registry_add_from_string does NOT enforce the purpose ↔ script-type
// convention. Any descriptor parseable by libwally with our fingerprint in
// one of the keys is addable. The caller (UI) is expected to have already
// shown a "non-standard purpose/script combination" warning when
// `purpose_script_binding_check_soft(...)` returned WARN; this function
// just does the storage + parse.
bool registry_add_from_string(const char *id, const char *descriptor_str,
                              storage_location_t loc, bool persist);
bool registry_remove(const char *id);

// Wipe in-memory set. Called on wallet_unload().
void registry_clear(void);
```

---

## Snip 03 — `wallet.h` after shrinking

```c
bool wallet_init(wallet_network_t network);  // now only records network + triggers registry_init
bool wallet_is_initialized(void);
wallet_network_t wallet_get_network(void);
void wallet_cleanup(void);
void wallet_unload(void);
```

---

## Snip 04 — `settings.h` additions

```c
bool settings_get_permissive_signing(void);
esp_err_t settings_set_permissive_signing(bool permissive);
```

Default = `false` (strict / refuse).

---

## Snip 05 — PSBT helpers (types and function declarations)

```c
// Shared PSBT utility: extract the UTXO scriptPubKey for an input.
// Returns false if neither witness_utxo nor non_witness_utxo is present
// (or non_witness_utxo is present but the referenced prevout is out of
// range). Without this we cannot verify and MUST refuse to sign.
bool psbt_input_utxo_script(const struct wally_psbt *psbt, size_t input_i,
                            unsigned char *out, size_t out_cap, size_t *out_len);

// Try the whitelist. Fills `claim_out` on success.
typedef struct {
  enum { CLAIM_WHITELIST, CLAIM_REGISTRY } kind;
  union {
    ss_keypath_t ss;                       // CLAIM_WHITELIST
    struct {                                // CLAIM_REGISTRY
      const registry_entry_t *entry;
      uint32_t multi_index;  // 0 or 1
      uint32_t child_num;
    } reg;
  };
} claim_t;

bool try_match_whitelist(const unsigned char *keypath, size_t keypath_len,
                         bool is_testnet, claim_t *claim_out);

bool try_match_registry(const unsigned char *keypath, size_t keypath_len,
                        claim_t *claim_out);

// Regenerate the expected scripts for a claim.
typedef struct {
  unsigned char spk[WALLY_SCRIPTPUBKEY_P2WSH_LEN];
  size_t spk_len;
  // For sh(wpkh): the redeem-script (0x0014 <pkh>) we expect in the PSBT.
  unsigned char redeem[22];
  size_t redeem_len;   // 0 if not sh(wpkh)
  // For wsh / miniscript: the witness-script; regeneration uses
  // wally_descriptor_to_script_get_*. 0 if not wsh.
  unsigned char witness[WALLY_WITNESSSCRIPT_MAX_LEN];
  size_t witness_len;
} expected_scripts_t;

bool claim_regenerate(const claim_t *c, bool is_testnet,
                      expected_scripts_t *out);
```

---

## Snip 06 — `try_match_whitelist` algorithm

```
if keypath_len != 4 + 5*4 (= 24): return false
components[i] = u32_le(keypath + 4 + 4*i)  for i in 0..5

if !hardened(components[0..3]):             return false
if  hardened(components[3..5]):             return false

purpose = unharden(components[0])
script  = { 44→P2PKH, 49→P2SH_P2WPKH, 84→P2WPKH, 86→P2TR }[purpose]
            or return false

coin    = unharden(components[1])
if is_testnet && coin != 1: return false
if !is_testnet && coin != 0: return false

account = unharden(components[2])
if account >= SS_MAX_ACCOUNT: return false

chain   = components[3]
if chain > 1: return false

index   = components[4]
if index >= SS_MAX_ADDR_INDEX: return false

*claim_out = { kind=CLAIM_WHITELIST, ss=...(filled) }
return true
```

---

## Snip 07 — `try_match_registry` algorithm

```
// keypath layout: [fp(4)][origin components][trailing components]
// Total BIP32 depth ≤ MAX_KEYPATH_TOTAL_DEPTH (8).

if (keypath_len - 4) % 4 != 0: return false
total_depth = (keypath_len - 4) / 4
if total_depth > MAX_KEYPATH_TOTAL_DEPTH: return false

for each registry entry e:
  if e->origin_path_len > total_depth: continue
  // Byte-compare the first `e->origin_path_len` components.
  if memcmp(keypath + 4,
            e->origin_path,
            e->origin_path_len * 4) != 0: continue

  tail_depth = total_depth - e->origin_path_len
  if tail_depth != MAX_KEYPATH_TAIL_DEPTH (= 2): continue  // require <mp>/<i>

  mp = u32_le(keypath + 4 + 4*e->origin_path_len)
  ix = u32_le(keypath + 4 + 4*(e->origin_path_len + 1))

  if hardened(mp) || hardened(ix): continue
  if mp > 1: continue
  // If the descriptor is not multipath, only mp == 0 is valid.
  if e->num_paths == 1 && mp != 0: continue

  *claim_out = { kind=CLAIM_REGISTRY, reg={e, mp, ix} };
  return true

return false
```

Note on duplicates: multiple entries may share an origin prefix for our
key. The matcher returns the first hit; callers iterate, regenerate, and
if the verify step fails they call the matcher again with a `start_index`
cursor so they can move past the false positive.

---

## Snip 08 — `claim_regenerate` per script type

```
// SingleSigClaim
if c.kind == CLAIM_WHITELIST:
   path = "m/purpose'/coin'/account'/chain/index"  (ss_keypath_format)
   key  = key_get_derived_key(path)
   pk33 = key->pub_key   // compressed 33-byte pubkey

   switch c.ss.script:
     P2PKH:
        hash160(pk33) → pkh20
        out.spk      = OP_DUP OP_HASH160 <20> pkh20 OP_EQUALVERIFY OP_CHECKSIG
        out.redeem_len = 0; out.witness_len = 0

     P2WPKH:
        hash160(pk33) → pkh20
        out.spk      = OP_0 <20> pkh20        (via wally_witness_program_from_bytes)
        out.redeem_len = 0; out.witness_len = 0

     P2SH_P2WPKH:
        hash160(pk33)            → pkh20
        wpkh_script = OP_0 <20> pkh20
        hash160(wpkh_script)     → sh20
        out.spk      = OP_HASH160 <20> sh20 OP_EQUAL
        out.redeem   = wpkh_script (22 bytes, redeem_len=22)
        out.witness_len = 0

     P2TR:
        x_only = pk33[1..33]                  // 32-byte x-only
        tweak  = bip341_tweak(x_only, /*no script tree*/)
        out.spk      = OP_1 <32> tweak        (via wally_scriptpubkey_p2tr_from_bytes
                                               or manual)
        out.redeem_len = 0; out.witness_len = 0

// DescriptorClaim
if c.kind == CLAIM_REGISTRY:
   wally_descriptor_to_script(
       c.reg.entry->desc,
       0 /*depth*/, c.reg.multi_index, c.reg.child_num,
       0 /*variant*/, 0 /*flags*/,
       out.spk, sizeof(out.spk), &out.spk_len)

   // For wsh(...) and sh(wsh(...)), libwally can also emit the witness /
   // redeem scripts at that index via wally_descriptor_to_script with the
   // appropriate depth argument (depth=1 yields the inner script). These
   // populate out.witness / out.redeem for the post-regenerate comparison
   // against the PSBT's witness_script / redeem_script fields.
```

---

## Snip 09 — `psbt_classify_input`

```
classify_input(psbt, i, is_testnet) -> input_ownership_t:
  if !psbt_input_utxo_script(psbt, i, utxo_script):
    return NOT_OURS  // cannot safely sign without the UTXO script

  seen_our_fp = false
  for each keypath j in input i:
    kp = wally_psbt_get_input_keypath(psbt, i, j)
    if !starts_with_our_fp(kp): continue
    seen_our_fp = true

    // Try whitelist first, then registry. Registry matcher supports paging
    // so we can iterate if the first entry fails verification.
    for claim in enumerate_claims(kp):
      if !claim_regenerate(&claim, is_testnet, &exp): continue
      if !equal(exp.spk, utxo_script): continue

      // Auxiliary checks — non-seg witnesses vs witnessScript vs redeemScript
      if exp.redeem_len > 0:
        if !psbt_input_redeem_script_equals(psbt, i, exp.redeem): continue
      if exp.witness_len > 0:
        if !psbt_input_witness_script_equals(psbt, i, exp.witness): continue

      return { owned=true, verified=true, claim=claim }

  if seen_our_fp:
    if settings_get_permissive_signing():
      return { owned=true, verified=false, requires_ack=true,
               keypaths_snapshot=... }
    return NOT_OURS          // fingerprint matched but no verifiable claim
  return NOT_OURS
```

---

## Snip 10 — signing loop (replaces `psbt_sign` body)

```
for each input i:
  c = classify_input(psbt, i, is_testnet)
  if c.owned == false: continue

  if c.verified == false:
    // permissive path — ask user
    if !ui_ack_unknown_input(i, c.keypaths_snapshot): continue
    // pick the first fp-matching keypath; derive straight from its full path
    path = bip32_path_string_from_keypath(first_fp_keypath)
  else if c.claim.kind == CLAIM_WHITELIST:
    path = ss_keypath_format(&c.claim.ss)
  else:
    path = format_registry_path(c.claim.reg.entry, c.claim.reg.multi_index,
                                c.claim.reg.child_num)

  key = key_get_derived_key(path)
  wally_psbt_sign(psbt, key->priv_key+1, 32, EC_FLAG_GRIND_R)
```

Self-cosign edge case: if a single input has two fp-matching keypaths that
each produce a verified claim (at different positions in a registered
descriptor), capture all verified claims rather than breaking on the first
— then call `wally_psbt_sign` once per claim's derived key.

---

## Snip 11 — `psbt_classify_output`

A signer does not have a "change vs receive" concept; it only decides
whether an output is owned by this wallet. The wallet-UX notion of change
(chain == 1) lives in the Addresses page, not in the classifier.

```
classify_output(psbt, global_tx, i, is_testnet) -> output_ownership_t:
  out_script = global_tx->outputs[i].script

  for each output keypath j:
    kp = wally_psbt_get_output_keypath(psbt, i, j)
    if !starts_with_our_fp(kp): continue

    for claim in enumerate_claims(kp):
      if !claim_regenerate(&claim, is_testnet, &exp): continue
      if !equal(exp.spk, out_script): continue
      return { owned=true, source=claim }   // no is_change, no change/receive

  return NOT_OURS   // external destination; fingerprint-only fallback
                    // (old psbt.c:232-234 behavior) is intentionally dropped
```

The review UI can still read derivation coordinates out of `source` for
display (e.g. show the full path `m/84'/0'/0'/1/7` next to the amount), but
it must not label the output as "change" or "receive" — that's a wallet
convention, not a signer fact.

---

## Snip 12 — boot wiring before/after

Today (`main/pages/shared/key_confirmation.c:25-46`):

```
settings_get_default_network()
settings_get_default_policy()
wallet_set_policy(...)
wallet_init(net)
```

After rework:

```
net = settings_get_default_network()
wallet_init(net)
registry_init(net == WALLET_NETWORK_TESTNET)
```
