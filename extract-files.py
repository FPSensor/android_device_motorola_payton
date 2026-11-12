#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools

extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_9'

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/motorola/payton',
    'device/motorola/sdm660-common',
    # Kernel 4.19 (QSSI) uses the sdm660 HALs
    'hardware/qcom-caf/sdm660',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/display',
    'hardware/qcom-caf/wlan',
    'vendor/motorola/sdm660-common',
    'vendor/qcom/opensource/dataservices',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

# The camera HAL links android.frameworks.displayservice@1.0, which is gone:
# point it at the lineage.frameworks copy, and resolve the HIDL methods that
# library does not export to IEventCallback::ping, as ginkgo does.
_displayservice_ping = (
    b'_ZN7lineage10frameworks14displayservice4V1_014IEventCallback4pingEv'
)
_displayservice_unresolved = (
    rb'_ZN7lineage10frameworks14displayservice4V1_01[45]I[A-Za-z0-9_]*'
    rb'(?:linkToDeath|unlinkToDeath|getDebugInfo|getHashChain|'
    rb'interfaceChain|interfaceDescriptor|5debug|registerForNotifications)'
    rb'[A-Za-z0-9_]*'
)

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/hw/android.hardware.biometrics.fingerprint@2.1-fpcservice': blob_fixup()
        .replace_needed('com.fingerprints.extension@1.0_vendor.so', 'com.fingerprints.extension@1.0.so')
        .binary_regex_replace(b'/sys/devices/soc\x00', b'/dev/fpc_soc\x00\x00\x00\x00\x00'),
    'vendor/bin/charge_only_mode': blob_fixup()
        .add_needed('libmemset_shim.so'),
    # The Pie HAL reads private_handle_t::size and ::offset at their gralloc1
    # (kernel 4.4 display HAL) offsets, 52 and 56. With the 4.19 gralloc
    # they live at 72 and 76, and offset 52 holds layer_count, so every
    # gralloc buffer was mapped one page long and the JPEG encoder crashed
    # writing past it. QCamera3GrallocMemory::registerBuffer: the ldrd
    # feeding a debug log and the ldr feeding the mmap length.
    'vendor/lib/hw/camera.sdm660.so': blob_fixup()
        .binary_regex_replace(b'\xca\x68\xd1\xe9\x0d\x31\x04\x91', b'\xca\x68\xd1\xe9\x12\x31\x04\x91')
        .binary_regex_replace(b'\x4f\xf0\x00\x08\x40\x6b\xc8\x60', b'\x4f\xf0\x00\x08\x80\x6c\xc8\x60')
        .replace_needed('android.frameworks.displayservice@1.0.so',
                        'lineage.frameworks.displayservice@1.0.so')
        .binary_regex_replace(
            b'7android10frameworks14displayservice',
            b'7lineage10frameworks14displayservice')
        .binary_regex_replace(
            _displayservice_unresolved,
            lambda m: _displayservice_ping.ljust(len(m.group(0)), b'\x00')),
    'vendor/etc/init/android.hardware.biometrics.fingerprint@2.1-service-payton.rc': blob_fixup()
        .regex_replace('system input', 'system uhid input'),
    (
        'vendor/lib/libdualcameraddm.so',
        'vendor/lib/libmmcamera_hdr_gb_lib.so',
        'vendor/lib/libvideobokeh.so',
        'vendor/lib64/libdualcameraddm.so',
        'vendor/lib64/libvideobokeh.so'
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'vendor/lib/libmmcamera2_pproc_modules.so': blob_fixup()
        .binary_regex_replace(b'\x70\x72\x6F\x64\x75\x63\x74\x2E\x6D\x61\x6E\x75', b'\x70\x72\x6F\x64\x75\x63\x74\x2E\x6E\x6F\x70\x65'),
    'vendor/lib/libzaf_core.so': blob_fixup()
        .binary_regex_replace(b'\x2f\x73\x79\x73\x74\x65\x6d\x2f\x65\x74\x63\x2f\x7a\x61\x66', b'\x2f\x76\x65\x6e\x64\x6f\x72\x2f\x65\x74\x63\x2f\x7a\x61\x66'),
    'vendor/lib64/vendor.qti.hardware.tui_comm@1.0.so': blob_fixup()
        .replace_needed('libhidlbase.so', 'libhidlbase-v32.so')
        .replace_needed('libutils.so', 'libutils-v32.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'payton',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(module, 'sdm660-common', module.vendor)
    utils.run()
