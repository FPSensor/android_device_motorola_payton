#
# Copyright (C) 2017 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Must set these before including common config
TARGET_BOARD_PLATFORM := sdm660
TARGET_BOOTLOADER_BOARD_NAME := SDM660

# Inherit from motorola sdm660-common
include device/motorola/sdm660-common/BoardConfigCommon.mk

DEVICE_PATH := device/motorola/payton

# A/B updater
AB_OTA_PARTITIONS += \
    boot \
    system \
    vendor

AB_OTA_UPDATER := true

# Assertions
TARGET_BOARD_INFO_FILE := $(DEVICE_PATH)/board-info.txt
TARGET_OTA_ASSERT_DEVICE := payton

# Display
TARGET_SCREEN_DENSITY := 420

# SELinux
BOARD_VENDOR_SEPOLICY_DIRS += $(DEVICE_PATH)/sepolicy/vendor

# Kernel
BOARD_KERNEL_CMDLINE += androidboot.boot_devices=soc/c0c4000.sdhci
TARGET_KERNEL_CONFIG := \
    vendor/sdm660-perf_defconfig \
    vendor/ext_config/moto-sdm660.config \
    vendor/ext_config/payton.config

# Early kernel logs on the debug UART (BLSP1 UART2, gpio4/5, 115200 8N1).
# Off by default: a serial console slows down boot.
ifeq ($(TARGET_PAYTON_UART_LOG),true)
# The UART driver node is disabled in the DT (its console clock vote blocks
# XO shutdown), so keep the early console alive for the whole boot instead.
BOARD_KERNEL_CMDLINE += earlycon=msm_serial_dm,0xc170000 keep_bootcon
else
# Without any console= the kernel enables the first tty console that
# registers, which is the debug UART. console=null leaves init without a
# console and crashes it, so keep the UART but only print critical
# messages on consoles: at 115200 baud a full boot log storm stalls
# printk with interrupts off. The log buffer still keeps everything.
BOARD_KERNEL_CMDLINE += loglevel=3
endif

# HIDL
DEVICE_MANIFEST_FILE += $(DEVICE_PATH)/payton_manifest.xml

# Partitions
BOARD_BOOTIMAGE_PARTITION_SIZE := 67108864
BOARD_SYSTEMIMAGE_PARTITION_SIZE := 4328521728
BOARD_VENDORIMAGE_PARTITION_SIZE := 603979776

# Power
TARGET_HAS_NO_WLAN_STATS := true

# Properties
TARGET_SYSTEM_EXT_PROP += $(DEVICE_PATH)/system_ext.prop
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop

# RIL
ENABLE_VENDOR_RIL_SERVICE := true

# inherit from the proprietary version
include vendor/motorola/payton/BoardConfigVendor.mk
