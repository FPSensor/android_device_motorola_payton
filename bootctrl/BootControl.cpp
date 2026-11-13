/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include "BootControl.h"

#include <string>

#include "boot_control.h"

using ndk::ScopedAStatus;

namespace aidl::android::hardware::boot {

namespace {

ScopedAStatus InvalidSlot(int32_t slot) {
    return ScopedAStatus::fromServiceSpecificErrorWithMessage(
            IBootControl::INVALID_SLOT, ("Invalid slot " + std::to_string(slot)).c_str());
}

ScopedAStatus CommandFailed() {
    return ScopedAStatus::fromServiceSpecificErrorWithMessage(IBootControl::COMMAND_FAILED,
                                                              "Operation failed");
}

}  // namespace

ScopedAStatus BootControl::getActiveBootSlot(int32_t* _aidl_return) {
    *_aidl_return = get_active_boot_slot();
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::getCurrentSlot(int32_t* _aidl_return) {
    *_aidl_return = get_current_slot();
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::getNumberSlots(int32_t* _aidl_return) {
    *_aidl_return = get_number_slots();
    return ScopedAStatus::ok();
}

// payton has no Virtual A/B, so there is never a snapshot to merge.
ScopedAStatus BootControl::getSnapshotMergeStatus(MergeStatus* _aidl_return) {
    *_aidl_return = MergeStatus::NONE;
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::setSnapshotMergeStatus(MergeStatus in_status) {
    if (in_status != MergeStatus::NONE) {
        return CommandFailed();
    }
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::getSuffix(int32_t in_slot, std::string* _aidl_return) {
    // Like the HIDL HAL, return an empty string for an invalid slot.
    const char* suffix = in_slot < 0 ? nullptr : get_suffix(in_slot);
    if (suffix) {
        *_aidl_return = suffix;
    } else {
        _aidl_return->clear();
    }
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::isSlotBootable(int32_t in_slot, bool* _aidl_return) {
    int ret = in_slot < 0 ? -1 : is_slot_bootable(in_slot);
    if (ret < 0) {
        return InvalidSlot(in_slot);
    }
    *_aidl_return = ret != 0;
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::isSlotMarkedSuccessful(int32_t in_slot, bool* _aidl_return) {
    int ret = in_slot < 0 ? -1 : is_slot_marked_successful(in_slot);
    if (ret < 0) {
        return InvalidSlot(in_slot);
    }
    *_aidl_return = ret != 0;
    return ScopedAStatus::ok();
}

ScopedAStatus BootControl::markBootSuccessful() {
    return mark_boot_successful() == 0 ? ScopedAStatus::ok() : CommandFailed();
}

ScopedAStatus BootControl::setActiveBootSlot(int32_t in_slot) {
    if (in_slot < 0) {
        return InvalidSlot(in_slot);
    }
    return set_active_boot_slot(in_slot) == 0 ? ScopedAStatus::ok() : CommandFailed();
}

ScopedAStatus BootControl::setSlotAsUnbootable(int32_t in_slot) {
    if (in_slot < 0) {
        return InvalidSlot(in_slot);
    }
    return set_slot_as_unbootable(in_slot) == 0 ? ScopedAStatus::ok() : CommandFailed();
}

}  // namespace aidl::android::hardware::boot
