#include "registry.h"
#include <string.h>

static registry_entry_t registry_entries[REGISTRY_MAX_ENTRIES];
static size_t registry_len = 0;

size_t registry_count(void) {
  return registry_len;
}

const registry_entry_t *registry_get(size_t i) {
  if (i >= registry_len) return NULL;
  return &registry_entries[i];
}

const registry_entry_t *registry_find_by_id(const char *id) {
  for (size_t i = 0; i < registry_len; i++) {
    if (strncmp(registry_entries[i].id, id, REGISTRY_ID_MAX_LEN) == 0) {
      return &registry_entries[i];
    }
  }
  return NULL;
}

void registry_clear(void) {
  for (size_t i = 0; i < registry_len; i++) {
    if (registry_entries[i].desc != NULL) {
      wally_descriptor_free(registry_entries[i].desc);
    }
  }
  memset(registry_entries, 0, sizeof registry_entries);
  registry_len = 0;
}
