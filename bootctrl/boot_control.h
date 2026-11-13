/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#ifdef __cplusplus
extern "C" {
#endif

// Slot handling of the legacy bootctrl.qcom HAL, which keeps the A/B state
// in the GPT attributes the way the payton bootloader expects it.
unsigned get_number_slots(void);
unsigned get_current_slot(void);
unsigned get_active_boot_slot(void);
int mark_boot_successful(void);
int set_active_boot_slot(unsigned slot);
int set_slot_as_unbootable(unsigned slot);
int is_slot_bootable(unsigned slot);
int is_slot_marked_successful(unsigned slot);
const char *get_suffix(unsigned slot);

#ifdef __cplusplus
}
#endif
