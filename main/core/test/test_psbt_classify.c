#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

/* Wally types needed by stubs */
#include <wally_bip32.h>

/* Project headers for stub type declarations */
#include "core/storage.h"
#include "core/key.h"
#include "core/wallet.h"
#include "core/registry.h"

/* --- Storage stubs (registry.c persist=false path never calls these) --- */
esp_err_t storage_save_descriptor(storage_location_t loc, const char *id,
                                   const uint8_t *data, size_t len,
                                   bool encrypted) {
  (void)loc; (void)id; (void)data; (void)len; (void)encrypted;
  return ESP_OK;
}
esp_err_t storage_delete_descriptor(storage_location_t loc,
                                     const char *filename) {
  (void)loc; (void)filename;
  return ESP_OK;
}
esp_err_t storage_list_descriptors(storage_location_t loc,
                                    char ***filenames_out, int *count_out) {
  (void)loc;
  if (filenames_out) *filenames_out = NULL;
  if (count_out) *count_out = 0;
  return ESP_OK;
}
esp_err_t storage_load_descriptor(storage_location_t loc, const char *filename,
                                   uint8_t **data_out, size_t *len_out,
                                   bool *encrypted_out) {
  (void)loc; (void)filename;
  if (data_out) *data_out = NULL;
  if (len_out) *len_out = 0;
  if (encrypted_out) *encrypted_out = false;
  return -1;
}
void storage_free_file_list(char **files, int count) {
  (void)files; (void)count;
}

/* --- Wallet stubs --- */
uint32_t         wallet_get_account(void)                      { return 0; }
wallet_network_t wallet_get_network(void)                      { return WALLET_NETWORK_MAINNET; }
bool             wallet_has_descriptor(void)                   { return false; }
bool wallet_get_multisig_receive_address(uint32_t i, char **a) { (void)i; (void)a; return false; }
bool wallet_get_multisig_change_address(uint32_t i, char **a)  { (void)i; (void)a; return false; }

/* --- Key: real implementation but key_get_fingerprint always returns 00000000.
 *
 * Registry tests need fingerprint 00000000 to match descriptors that use
 * [00000000/...].  Whitelist tests use key_get_derived_key (real) and never
 * call key_get_fingerprint.  Rename the real function so we can define the
 * stub after the include without a redefinition error. --- */
#define key_get_fingerprint key_get_fingerprint_raw
#include "../key.c"
#undef key_get_fingerprint

bool key_get_fingerprint(unsigned char *fp) {
  if (fp) memset(fp, 0, BIP32_KEY_FINGERPRINT_LEN);
  return true;
}

#include "../ss_whitelist.c"

#define TAG registry_TAG
#include "../registry.c"
#undef TAG

#define TAG psbt_TAG
#include "../psbt.c"
#undef TAG

/* ------------------------------------------------------------------ */

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name)  printf("Testing: %s... ", name)
#define PASS()      do { printf("PASS\n"); tests_passed++; } while (0)
#define FAIL(msg)   do { printf("FAIL: %s\n", msg); tests_failed++; } while (0)

/* ================================================================
 * Whitelist tests
 * ================================================================ */

static const char *TEST_MNEMONIC =
    "abandon abandon abandon abandon abandon abandon "
    "abandon abandon abandon abandon abandon about";

static const uint8_t REF_SPK_P2PKH[] = {
    0x76, 0xa9, 0x14,
    0xd9, 0x86, 0xed, 0x01, 0xb7, 0xa2, 0x22, 0x25,
    0xa7, 0x0e, 0xdb, 0xf2, 0xba, 0x7c, 0xfb, 0x63,
    0xa1, 0x5c, 0xb3, 0xaa,
    0x88, 0xac
};

static const uint8_t REF_SPK_P2SH_P2WPKH[] = {
    0xa9, 0x14,
    0x3f, 0xb6, 0xe9, 0x58, 0x12, 0xe5, 0x7b, 0xb4,
    0x69, 0x1f, 0x9a, 0x4a, 0x62, 0x88, 0x62, 0xa6,
    0x1a, 0x4f, 0x76, 0x9b,
    0x87
};

static const uint8_t REF_SPK_P2WPKH[] = {
    0x00, 0x14,
    0xc0, 0xce, 0xbc, 0xd6, 0xc3, 0xd3, 0xca, 0x8c,
    0x75, 0xdc, 0x5e, 0xc6, 0x2e, 0xbe, 0x55, 0x33,
    0x0e, 0xf9, 0x10, 0xe2
};

static const uint8_t REF_SPK_P2TR[] = {
    0x51, 0x20,
    0xa6, 0x08, 0x69, 0xf0, 0xdb, 0xcf, 0x1d, 0xc6,
    0x59, 0xc9, 0xce, 0xcb, 0xaf, 0x80, 0x50, 0x13,
    0x5e, 0xa9, 0xe8, 0xcd, 0xc4, 0x87, 0x05, 0x3f,
    0x1d, 0xc6, 0x88, 0x09, 0x49, 0xdc, 0x68, 0x4c
};

static void test_whitelist_claim(const char *name, ss_script_type_t script,
                                  uint32_t purpose,
                                  const uint8_t *ref_spk, size_t ref_spk_len,
                                  bool expect_redeem) {
  TEST(name);
  claim_t claim = {0};
  claim.kind              = CLAIM_WHITELIST;
  claim.whitelist.script  = script;
  claim.whitelist.purpose = purpose;
  claim.whitelist.coin    = 0;
  claim.whitelist.account = 0;
  claim.whitelist.chain   = 0;
  claim.whitelist.index   = 0;

  expected_scripts_t out = {0};
  if (!claim_regenerate(&claim, false, &out)) {
    FAIL("claim_regenerate returned false"); return;
  }
  if (out.spk_len != ref_spk_len) {
    FAIL("wrong spk_len"); return;
  }
  if (memcmp(out.spk, ref_spk, ref_spk_len) != 0) {
    FAIL("spk bytes mismatch"); return;
  }
  if (expect_redeem && out.redeem_len != SS_P2SH_P2WPKH_REDEEM_LEN) {
    FAIL("wrong redeem_len for P2SH-P2WPKH"); return;
  }
  if (!expect_redeem && out.redeem_len != 0) {
    FAIL("non-zero redeem_len for non-P2SH type"); return;
  }
  if (expect_redeem && (out.redeem[0] != 0x00 || out.redeem[1] != 0x14)) {
    FAIL("redeem script does not start OP_0 <20>"); return;
  }
  if (out.witness_len != 0) {
    FAIL("witness_len should be 0"); return;
  }
  PASS();
}

/* ================================================================
 * Registry tests
 * ================================================================ */

#define XPUB_84 \
  "xpub6CatWdiZiodmUeTDp8LT5or8nmbKNcuyvz7WyksVFkKB4RHwCD3XyuvP" \
  "EbvqAQY3rAPshWcMLoP2fMFMKHPJ4ZeZXYVUhLv1VMrjPC7PW6V"
#define XPUB_86 \
  "xpub6BgBgsespWvERF3LHQu6CnqdvfEvtMcQjYrcRzx53QJjSxarj2afYWc" \
  "LteoGVky7D3UKDP9QyrLprQ3VCECoY49yfdDEHGCtMMj92pReUsQ"

/* --- Reference bytes (captured from print-mode run) --- */

/* wsh(sortedmulti(2-of-2)): P2WSH SPK, no redeem, sortedmulti witness */
static const uint8_t REF_WSH_SPK[] = {
    0x00, 0x20, 0xdc, 0x66, 0x81, 0xe3, 0x4b, 0x91, 0xcd, 0xf6,
    0x3f, 0x40, 0x08, 0xdb, 0x1f, 0x8b, 0xb0, 0x2d, 0x62, 0xf0,
    0x06, 0xa1, 0xd7, 0x46, 0x39, 0xc6, 0x56, 0xdf, 0x52, 0x61,
    0x96, 0x7f, 0xc2, 0xb1
};
static const uint8_t REF_WSH_WITNESS[] = {
    0x52,
    0x21, 0x03, 0x30, 0xd5, 0x4f, 0xd0, 0xdd, 0x42, 0x0a, 0x6e,
    0x5f, 0x8d, 0x36, 0x24, 0xf5, 0xf3, 0x48, 0x2c, 0xae, 0x35,
    0x0f, 0x79, 0xd5, 0xf0, 0x75, 0x3b, 0xf5, 0xbe, 0xef, 0x9c,
    0x2d, 0x91, 0xaf, 0x3c,
    0x21, 0x03, 0xcc, 0x8a, 0x4b, 0xc6, 0x4d, 0x89, 0x7b, 0xdd,
    0xc5, 0xfb, 0xc2, 0xf6, 0x70, 0xf7, 0xa8, 0xba, 0x0b, 0x38,
    0x67, 0x79, 0x10, 0x6c, 0xf1, 0x22, 0x3c, 0x6f, 0xc5, 0xd7,
    0xcd, 0x6f, 0xc1, 0x15,
    0x52, 0xae
};

/* sh(wsh(sortedmulti(2-of-2))): P2SH SPK, P2WSH redeem, same witness */
static const uint8_t REF_SHWSH_SPK[] = {
    0xa9, 0x14, 0x87, 0xbb, 0xc7, 0x92, 0xae, 0x98, 0xf0, 0x87,
    0x4a, 0x1c, 0x2e, 0xc9, 0x99, 0xc4, 0x55, 0x73, 0x6d, 0x9d,
    0x2b, 0xba, 0x87
};
/* REF_SHWSH_REDEEM is the P2WSH program — identical to REF_WSH_SPK */
static const uint8_t REF_SHWSH_WITNESS[] = {
    0x52,
    0x21, 0x03, 0x30, 0xd5, 0x4f, 0xd0, 0xdd, 0x42, 0x0a, 0x6e,
    0x5f, 0x8d, 0x36, 0x24, 0xf5, 0xf3, 0x48, 0x2c, 0xae, 0x35,
    0x0f, 0x79, 0xd5, 0xf0, 0x75, 0x3b, 0xf5, 0xbe, 0xef, 0x9c,
    0x2d, 0x91, 0xaf, 0x3c,
    0x21, 0x03, 0xcc, 0x8a, 0x4b, 0xc6, 0x4d, 0x89, 0x7b, 0xdd,
    0xc5, 0xfb, 0xc2, 0xf6, 0x70, 0xf7, 0xa8, 0xba, 0x0b, 0x38,
    0x67, 0x79, 0x10, 0x6c, 0xf1, 0x22, 0x3c, 0x6f, 0xc5, 0xd7,
    0xcd, 0x6f, 0xc1, 0x15,
    0x52, 0xae
};

/* sh(multi(2-of-2)): P2SH SPK, raw multi redeem, no witness */
static const uint8_t REF_SHMU_SPK[] = {
    0xa9, 0x14, 0x7d, 0xbf, 0x87, 0xe7, 0x0c, 0x23, 0x27, 0x49,
    0x95, 0x78, 0xd6, 0xfb, 0xa1, 0xe4, 0x8a, 0x1f, 0xe8, 0xd1,
    0xe3, 0x44, 0x87
};
static const uint8_t REF_SHMU_REDEEM[] = {
    0x52,
    0x21, 0x03, 0x30, 0xd5, 0x4f, 0xd0, 0xdd, 0x42, 0x0a, 0x6e,
    0x5f, 0x8d, 0x36, 0x24, 0xf5, 0xf3, 0x48, 0x2c, 0xae, 0x35,
    0x0f, 0x79, 0xd5, 0xf0, 0x75, 0x3b, 0xf5, 0xbe, 0xef, 0x9c,
    0x2d, 0x91, 0xaf, 0x3c,
    0x21, 0x03, 0xcc, 0x8a, 0x4b, 0xc6, 0x4d, 0x89, 0x7b, 0xdd,
    0xc5, 0xfb, 0xc2, 0xf6, 0x70, 0xf7, 0xa8, 0xba, 0x0b, 0x38,
    0x67, 0x79, 0x10, 0x6c, 0xf1, 0x22, 0x3c, 0x6f, 0xc5, 0xd7,
    0xcd, 0x6f, 0xc1, 0x15,
    0x52, 0xae
};

/* tr([00000000/86'/0'/0']XPUB_86/0/*) child_num=0: P2TR SPK, no redeem, no witness */
static const uint8_t REF_TR_SPK[] = {
    0x51, 0x20,
    0xa6, 0x08, 0x69, 0xf0, 0xdb, 0xcf, 0x1d, 0xc6,
    0x59, 0xc9, 0xce, 0xcb, 0xaf, 0x80, 0x50, 0x13,
    0x5e, 0xa9, 0xe8, 0xcd, 0xc4, 0x87, 0x05, 0x3f,
    0x1d, 0xc6, 0x88, 0x09, 0x49, 0xdc, 0x68, 0x4c
};

/* sh(wsh(pkh([00000000/49'/0'/0']XPUB_84/0/*))) child_num=0:
 * P2SH SPK, P2WSH redeem, P2PKH witness script.
 * wsh(wpkh()) is rejected by this libwally build (BUILD_MINIMAL);
 * sh(wsh(pkh())) exercises the identical claim_regenerate code path. */
static const uint8_t REF_SHWSH_PKH_SPK[] = {
    0xa9, 0x14, 0xfe, 0x3b, 0x8d, 0xe9, 0xe4, 0xda,
    0xda, 0x6f, 0x6e, 0x11, 0x27, 0xb0, 0xae, 0xf0,
    0x44, 0x40, 0x41, 0x9d, 0x36, 0xeb, 0x87
};
static const uint8_t REF_SHWSH_PKH_REDEEM[] = {
    0x00, 0x20, 0xd5, 0x23, 0x5c, 0x05, 0xc4, 0xfa,
    0xe0, 0x21, 0x87, 0xdf, 0xe8, 0x5b, 0xfc, 0x3f,
    0x4c, 0x8e, 0x4d, 0x1f, 0x34, 0x7e, 0xce, 0x42,
    0x34, 0xe3, 0x6d, 0x13, 0x96, 0x57, 0x8e, 0x21,
    0xe8, 0xbb
};
static const uint8_t REF_SHWSH_PKH_WITNESS[] = {
    0x76, 0xa9, 0x14, 0xc0, 0xce, 0xbc, 0xd6, 0xc3,
    0xd3, 0xca, 0x8c, 0x75, 0xdc, 0x5e, 0xc6, 0x2e,
    0xbe, 0x55, 0x33, 0x0e, 0xf9, 0x10, 0xe2, 0x88,
    0xac
};

/* ------------------------------------------------------------------ */

static void test_registry_claim(
    const char  *test_name,
    const char  *desc_str,
    uint32_t     multi_index,
    uint32_t     child_num,
    const uint8_t *ref_spk,     size_t ref_spk_len,
    const uint8_t *ref_redeem,  size_t ref_redeem_len,
    const uint8_t *ref_witness, size_t ref_witness_len)
{
  TEST(test_name);
  registry_clear();
  if (!registry_add_from_string("t", desc_str, STORAGE_FLASH, false)) {
    FAIL("registry_add_from_string"); return;
  }
  const registry_entry_t *e = registry_find_by_id("t");
  if (!e) { FAIL("entry not found"); return; }

  claim_t claim = {0};
  claim.kind                 = CLAIM_REGISTRY;
  claim.registry.entry       = (registry_entry_t *)e;
  claim.registry.multi_index = multi_index;
  claim.registry.child_num   = child_num;

  expected_scripts_t out = {0};
  if (!claim_regenerate(&claim, false, &out)) { FAIL("claim_regenerate returned false"); return; }

  if (out.spk_len != ref_spk_len)                               { FAIL("spk_len mismatch");     return; }
  if (memcmp(out.spk, ref_spk, ref_spk_len) != 0)              { FAIL("spk bytes mismatch");    return; }
  if (out.redeem_len != ref_redeem_len)                         { FAIL("redeem_len mismatch");   return; }
  if (ref_redeem_len > 0 &&
      memcmp(out.redeem, ref_redeem, ref_redeem_len) != 0)      { FAIL("redeem mismatch");       return; }
  if (out.witness_len != ref_witness_len)                       { FAIL("witness_len mismatch");  return; }
  if (ref_witness_len > 0 &&
      memcmp(out.witness, ref_witness, ref_witness_len) != 0)   { FAIL("witness mismatch");      return; }
  PASS();
}

/* ------------------------------------------------------------------ */

int main(void) {
  printf("=== claim_regenerate whitelist tests ===\n\n");

  TEST("key_load_from_mnemonic");
  if (!key_load_from_mnemonic(TEST_MNEMONIC, "", false)) {
    FAIL("failed to load mnemonic");
    printf("\n=== ABORT ===\n");
    return 1;
  }
  PASS();

  test_whitelist_claim("P2PKH spk+redeem",       SS_SCRIPT_P2PKH,       44,
                       REF_SPK_P2PKH,       sizeof(REF_SPK_P2PKH),       false);
  test_whitelist_claim("P2SH-P2WPKH spk+redeem", SS_SCRIPT_P2SH_P2WPKH, 49,
                       REF_SPK_P2SH_P2WPKH, sizeof(REF_SPK_P2SH_P2WPKH), true);
  test_whitelist_claim("P2WPKH spk+redeem",       SS_SCRIPT_P2WPKH,      84,
                       REF_SPK_P2WPKH,      sizeof(REF_SPK_P2WPKH),      false);
  test_whitelist_claim("P2TR spk+redeem",          SS_SCRIPT_P2TR,        86,
                       REF_SPK_P2TR,        sizeof(REF_SPK_P2TR),         false);

  key_unload();

  printf("\n=== claim_regenerate registry tests ===\n\n");

  test_registry_claim(
      "wsh(sortedmulti 2-of-2)",
      "wsh(sortedmulti(2,"
      "[00000000/48'/0'/0'/2']" XPUB_84 "/0/*,"
      "[11111111/48'/0'/0'/2']" XPUB_86 "/0/*"
      "))#6nfc46dh",
      0, 0,
      REF_WSH_SPK,     sizeof(REF_WSH_SPK),
      NULL,            0,
      REF_WSH_WITNESS, sizeof(REF_WSH_WITNESS));

  test_registry_claim(
      "sh(wsh(sortedmulti 2-of-2))",
      "sh(wsh(sortedmulti(2,"
      "[00000000/48'/0'/0'/2']" XPUB_84 "/0/*,"
      "[11111111/48'/0'/0'/2']" XPUB_86 "/0/*"
      ")))",
      0, 0,
      REF_SHWSH_SPK,     sizeof(REF_SHWSH_SPK),
      REF_WSH_SPK,       sizeof(REF_WSH_SPK),   /* P2WSH redeem == WSH SPK */
      REF_SHWSH_WITNESS, sizeof(REF_SHWSH_WITNESS));

  test_registry_claim(
      "sh(multi(2-of-2))",
      "sh(multi(2,"
      "[00000000/48'/0'/0'/1']" XPUB_84 "/0/*,"
      "[11111111/48'/0'/0'/1']" XPUB_86 "/0/*"
      "))",
      0, 0,
      REF_SHMU_SPK,    sizeof(REF_SHMU_SPK),
      REF_SHMU_REDEEM, sizeof(REF_SHMU_REDEEM),
      NULL,            0);

  test_registry_claim(
      "tr([00000000/86'/0'/0']xpub/0/*)",
      "tr([00000000/86'/0'/0']" XPUB_86 "/0/*)",
      0, 0,
      REF_TR_SPK, sizeof(REF_TR_SPK),
      NULL,       0,
      NULL,       0);

  test_registry_claim(
      "sh(wsh(pkh([00000000/49'/0'/0']xpub/0/*)))",
      "sh(wsh(pkh([00000000/49'/0'/0']" XPUB_84 "/0/*)))",
      0, 0,
      REF_SHWSH_PKH_SPK,     sizeof(REF_SHWSH_PKH_SPK),
      REF_SHWSH_PKH_REDEEM,  sizeof(REF_SHWSH_PKH_REDEEM),
      REF_SHWSH_PKH_WITNESS, sizeof(REF_SHWSH_PKH_WITNESS));

  printf("\n=== Results: %d passed, %d failed ===\n",
         tests_passed, tests_failed);
  return tests_failed > 0 ? 1 : 0;
}
