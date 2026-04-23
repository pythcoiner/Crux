#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include "core/wallet.h"
#include "core/registry.h"

wallet_network_t wallet_get_network(void) { return WALLET_NETWORK_MAINNET; }
registry_entry_t *registry_match_keypath(const uint8_t *kp, size_t kp_len,
                                         size_t *cursor) {
  (void)kp; (void)kp_len; (void)cursor;
  return NULL;
}
