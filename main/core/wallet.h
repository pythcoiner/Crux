#ifndef WALLET_H
#define WALLET_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum {
  WALLET_NETWORK_MAINNET = 0,
  WALLET_NETWORK_TESTNET = 1,
} wallet_network_t;

// Format derivation path: "m/84'/0'/0'" or "m/48'/0'/0'/2'"
int wallet_format_derivation_path(char *buf, size_t buf_size,
                                  bool is_multisig,
                                  wallet_network_t network, uint32_t account);

// Format compact derivation: "84h/0h/0h" or "48h/0h/0h/2h"
int wallet_format_derivation_compact(char *buf, size_t buf_size,
                                     bool is_multisig,
                                     wallet_network_t network,
                                     uint32_t account);

bool wallet_init(wallet_network_t network);
bool wallet_is_initialized(void);
wallet_network_t wallet_get_network(void);
void wallet_cleanup(void);
void wallet_unload(void);

// Descriptor management (registry-backed)
bool wallet_has_descriptor(void);
bool wallet_get_descriptor_string(char **output);
bool wallet_get_descriptor_checksum(char **output);

#endif // WALLET_H
