#ifndef SS_WHITELIST_H
#define SS_WHITELIST_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

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
  uint32_t account;        // 0..SS_MAX_ACCOUNT (unhardened)
  uint32_t chain;          // 0 or 1 (unhardened)
  uint32_t index;          // < SS_MAX_ADDR_INDEX (unhardened)
} ss_keypath_t;

#define SS_MAX_ACCOUNT          100
#define SS_MAX_ADDR_INDEX       100

#define MAX_KEYPATH_ORIGIN_DEPTH    6
#define MAX_KEYPATH_TAIL_DEPTH      2
#define MAX_KEYPATH_TOTAL_DEPTH     (MAX_KEYPATH_ORIGIN_DEPTH + MAX_KEYPATH_TAIL_DEPTH)

static inline bool ss_is_hardened(uint32_t component) {
  return (component & 0x80000000u) != 0;
}

static inline uint32_t ss_unharden(uint32_t component) {
  return component & 0x7fffffffu;
}

static inline uint32_t ss_u32_le(const unsigned char *bytes) {
  return (uint32_t)bytes[0]
       | ((uint32_t)bytes[1] << 8)
       | ((uint32_t)bytes[2] << 16)
       | ((uint32_t)bytes[3] << 24);
}

#endif // SS_WHITELIST_H
