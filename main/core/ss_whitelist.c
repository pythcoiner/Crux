#include "ss_whitelist.h"
#include "key.h"
#include <stdio.h>
#include <string.h>
#include <wally_bip32.h>
#include <wally_crypto.h>
#include <wally_script.h>

bool ss_keypath_parse(const unsigned char *keypath_after_fp,
                      size_t keypath_len_after_fp,
                      ss_keypath_t *out) {
  if (keypath_len_after_fp != 20)
    return false;

  uint32_t c[5];
  for (int i = 0; i < 5; i++)
    c[i] = ss_u32_le(keypath_after_fp + 4 * i);

  // First 3 must be hardened (purpose, coin, account)
  if (!ss_is_hardened(c[0]) || !ss_is_hardened(c[1]) || !ss_is_hardened(c[2]))
    return false;

  // Last 2 must NOT be hardened (chain, index)
  if (ss_is_hardened(c[3]) || ss_is_hardened(c[4]))
    return false;

  uint32_t purpose = ss_unharden(c[0]);
  ss_script_type_t script;
  switch (purpose) {
    case 44: script = SS_SCRIPT_P2PKH;       break;
    case 49: script = SS_SCRIPT_P2SH_P2WPKH; break;
    case 84: script = SS_SCRIPT_P2WPKH;      break;
    case 86: script = SS_SCRIPT_P2TR;        break;
    default:  return false;
  }

  out->script  = script;
  out->purpose = purpose;
  out->coin    = ss_unharden(c[1]);
  out->account = ss_unharden(c[2]);
  out->chain   = c[3];
  out->index   = c[4];
  return true;
}

bool ss_keypath_format(const ss_keypath_t *kp, char *buf, size_t buf_size) {
  int n = snprintf(buf, buf_size, "m/%u'/%u'/%u'/%u/%u",
                   kp->purpose, kp->coin, kp->account,
                   kp->chain, kp->index);
  return n >= 0 && (size_t)n < buf_size;
}

bool ss_keypath_is_whitelisted(const ss_keypath_t *kp, bool is_testnet) {
  if (kp->purpose != 44 && kp->purpose != 49 &&
      kp->purpose != 84 && kp->purpose != 86)
    return false;

  uint32_t expected_coin = is_testnet ? 1u : 0u;
  if (kp->coin != expected_coin)
    return false;

  if (kp->account >= SS_MAX_ACCOUNT)
    return false;

  if (kp->chain > 1)
    return false;

  if (kp->index >= SS_MAX_ADDR_INDEX)
    return false;

  return true;
}

bool ss_scriptpubkey(ss_script_type_t script, uint32_t account,
                     uint32_t chain, uint32_t index, bool is_testnet,
                     uint8_t *out, size_t *out_len) {
  switch (script) {
    case SS_SCRIPT_P2WPKH: {
      ss_keypath_t kp = {
        .script  = SS_SCRIPT_P2WPKH,
        .purpose = 84,
        .coin    = is_testnet ? 1u : 0u,
        .account = account,
        .chain   = chain,
        .index   = index,
      };
      char path[SS_KEYPATH_FMT_MAX];
      if (!ss_keypath_format(&kp, path, sizeof(path)))
        return false;

      struct ext_key *derived_key = NULL;
      if (!key_get_derived_key(path, &derived_key))
        return false;

      int ret = wally_witness_program_from_bytes(
          derived_key->pub_key, EC_PUBLIC_KEY_LEN,
          WALLY_SCRIPT_HASH160,
          out, 22, out_len);
      bip32_key_free(derived_key);
      return ret == WALLY_OK;
    }
    case SS_SCRIPT_P2PKH: {
      ss_keypath_t kp = {
        .script  = SS_SCRIPT_P2PKH,
        .purpose = 44,
        .coin    = is_testnet ? 1u : 0u,
        .account = account,
        .chain   = chain,
        .index   = index,
      };
      char path[SS_KEYPATH_FMT_MAX];
      if (!ss_keypath_format(&kp, path, sizeof(path)))
        return false;

      struct ext_key *derived_key = NULL;
      if (!key_get_derived_key(path, &derived_key))
        return false;

      uint8_t pkh20[HASH160_LEN];
      int ret = wally_hash160(
          derived_key->pub_key, EC_PUBLIC_KEY_LEN,
          pkh20, HASH160_LEN);
      bip32_key_free(derived_key);
      if (ret != WALLY_OK)
        return false;

      out[0]  = 0x76;               /* OP_DUP */
      out[1]  = 0xa9;               /* OP_HASH160 */
      out[2]  = 0x14;               /* push 20 bytes */
      memcpy(out + 3, pkh20, 20);   /* 20-byte hash160 */
      out[23] = 0x88;               /* OP_EQUALVERIFY */
      out[24] = 0xac;               /* OP_CHECKSIG */
      *out_len = 25;
      return true;
    }
    case SS_SCRIPT_P2SH_P2WPKH:
    case SS_SCRIPT_P2TR:
    default:
      return false;
  }
}
