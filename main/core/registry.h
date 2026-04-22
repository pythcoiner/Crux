#ifndef REGISTRY_H
#define REGISTRY_H

#include <stddef.h>
#include <stdint.h>

#include <wally_descriptor.h>

#include "ss_whitelist.h"
#include "storage.h"

#define REGISTRY_MAX_ENTRIES  16
#define REGISTRY_ID_MAX_LEN   32

typedef struct {
  char id[REGISTRY_ID_MAX_LEN];
  storage_location_t loc;
  struct wally_descriptor *desc;
  size_t my_key_index;
  size_t num_paths;
  uint32_t origin_path[MAX_KEYPATH_ORIGIN_DEPTH];
  size_t origin_path_len;
} registry_entry_t;

#endif // REGISTRY_H
