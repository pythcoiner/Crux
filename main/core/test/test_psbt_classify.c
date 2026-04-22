#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "../key.c"
#include "../ss_whitelist.c"
#include "../psbt.c"

static int tests_passed = 0;
static int tests_failed = 0;

#define TEST(name)  printf("Testing: %s... ", name)
#define PASS()      do { printf("PASS\n"); tests_passed++; } while (0)
#define FAIL(msg)   do { printf("FAIL: %s\n", msg); tests_failed++; } while (0)

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

  printf("\n=== Results: %d passed, %d failed ===\n",
         tests_passed, tests_failed);
  return tests_failed > 0 ? 1 : 0;
}
