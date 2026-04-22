#include "ss_whitelist.h"
#include <stdio.h>

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
