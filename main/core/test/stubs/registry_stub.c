#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "esp_err.h"
#include "core/storage.h"
#include "core/wallet.h"
#include <wally_bip32.h>

bool key_get_fingerprint(unsigned char *fp) {
    if (fp) memset(fp, 0, BIP32_KEY_FINGERPRINT_LEN);
    return true;
}
wallet_network_t wallet_get_network(void) { return WALLET_NETWORK_MAINNET; }

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
