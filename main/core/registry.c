#include "registry.h"

static registry_entry_t registry_entries[REGISTRY_MAX_ENTRIES];
static size_t registry_len = 0;
