import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Assets"

headers = ["ASSET", "Description", "Location", "Format", "Size", "Created", "Access", "Protection Attribute", "TS"]

data = [
    ["IFX_ROM_ROT_KEY","ECDSA Public Key is used exclusively for authenticating first provisioning RAM Applications (usually limited to TO_SORT RAM Application)","ROM_ROT_BOOT","Fixed","136","ROM Tape-out","R – all LCS\nW – N/A","Integrity (ROM)",""],
    ["BOOTROW","BOOTROW stores LCS related information (see also BOOTROW checksum stored in NVM)","OTP_ROT_BOOT","Fixed. Location in RRAM/SFLASH is HW defined","16","VIRGIN","R – all LCS\nW – all LCS","Integrity (checksum verified by BOOT Firmware)","No"],
    ["BOOTROW_CHECKSUM","BOOTROW checksum is updated when BOOTROW in OTP is updated. BOOT Firmware shall compute checksum when reading the BOOTROW and compare it with the stored checksum. The 4-byte BOOTROW checksum includes a checksum of BOOTROW OTP and the address of BOOTROW OTP.","S_SFLASH_R0","Fixed","4","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – all LCS","No","No"],
    ["BASIC_TRIMS","Basic trims for initial booting. Usually this would be limited to a few trim values (e.g. Band-Gap, IREF and clocks for RRAM or SFLASH read trims) (Space reserved for 10 pairs. See also Section 5.1.6)","S_SFLASH_R0","Fixed","88","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – VIRGIN, SORT, PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["BASIC_TRIMS_OTP","Basic trims for initial booting. Usually these would be SFLASH read trims (Space reserved for 10 pairs. See also Section 5.1.6)","[MXS22]: N/A\n[MXS40Sv2]: OTP_ROT_BOOT","Fixed","88","[MXS22]: N/A\n[MXS40Sv2]: PROV","R – all LCS\nW – PROV","Integrity (checksum verified by BOOT Firmware)","No"],
    ["FULL_TRIMS","Full trims (Typically, this could include around 80 trim pairs. Space reserved for 99 pairs. See also Section 5.1.6)","S_SFLASH_R0","Fixed","800","SORT","R – all LCS\nW – SORT, PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["PE_TE_SCRATCHPAD","Area reserved for PE/TE values saved between test insertions. This area is managed by TRIMS RAM Application or ATE. BOOT Firmware adds neither asset size nor the checksum.","S_SFLASH_R0","Custom - see Description","Product specific","SORT","R – all LCS\nW – all LCS","No","No"],
    ["DEVICE_RT_CFG_PUBLIC","Device runtime configurations (trims) applied by ROM_BOOT which are visible to customer SW as well.","NS_SFLASH_R0","Fixed","Product specific","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["DEVICE_RT_CFG_PUBLIC_2","Device runtime configurations (trims, multipliers, etc.) NOT applied by ROM_BOOT which are visible to customer SW. (includes 4-byte checksum)","NS_SFLASH_R0","Variable","Product specific","SORT","R – all LCS\nW – SORT, PROV","Integrity (composite hash, checksum verified by PDL drivers)","No"],
    ["RRAM_BOOT/FLASH_BOOT","RRAM_BOOT/FLASH_BOOT is locked in Factory.","S_SFLASH_R0","Custom - code image format","32K","SORT","R – all LCS\nW – SORT","Integrity (composite hash)","No"],
    ["IFX_ROT_KEY0","IFX RoT Public Key is used to verify the signature of RAM Application. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – [MXS22]: VIRGIN\n[MXS40Sv2]: SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_ROT_KEY1","The second IFX RoT Public Key is used if the first key (IFX_ROT_KEY0) is revoked. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – [MXS22]: VIRGIN\n[MXS40Sv2]: SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_ROT_KEY_REVOC","IFX RoT Public Key Revocation flag is used for revoking the first key (IFX_ROT_KEY0) if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Design dependent","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – VIRGIN, SORT, PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["IFX_ROT_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","[MXS22]: VIRGIN\n[MXS40Sv2]: SORT","R – all LCS\nW – VIRGIN, SORT, PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["DIE_ID","DIE_ID identifies LOT(3-byte) + WAFER(1-byte) + XY(2-byte) + SORT(1-byte) + DATE(3-byte) of DIE = (10-byte). (10-byte + 4-byte checksum)","NS_SFLASH_R0","Fixed","14","SORT","R – all LCS\nW – SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["L0_VERSION","versions of ROM_BOOT, RRAM_BOOT/FLASH_BOOT (8-byte*2 + 4-byte checksum)","NS_SFLASH_R0","Fixed","20","SORT","R – all LCS\nW – SORT, PROV","Integrity (composite hash)","No"],
    ["DEVICE_ID_TO","DEVICE_ID_TO identifies FAMILY_ID (2-byte) + SI_REVISION_ID (1-byte) = (3-byte). (3-byte + 4-byte checksum)","NS_SFLASH_R0","Fixed","7","SORT","R – all LCS\nW – SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["DEVICE_ID_MPN","DEVICE_ID_MPN identifies SILICON_ID (2-byte) = (2-byte). (2-byte + 4-byte checksum)","NS_SFLASH_R0","Fixed","6","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["BOOT_DEVICE_CFG","Device boot configurations, includes SRAM repair configuration (4-byte), base address of test application programmed into RRAM/SFLASH (4-byte), 5 reserved words. (4-byte + 4-byte + 20-byte + 4-byte checksum)","S_SFLASH_R0","Fixed","32","SORT","R – all LCS\nW – SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["TOC1","Table of Content 1 (includes 4-byte checksum)","S_SFLASH_R0","Fixed","Product specific","SORT","R – all LCS\nW – SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["TOC2","Table of Content 2 (includes 4-byte checksum)","S_SFLASH_R0","Fixed","Design dependent","PROV","R – all LCS\nW – PROV, NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["ASSET_HASH_LIST","List of assets included into ASSET_HASH (4-byte counter + 15*8-byte pairs + 4-byte checksum)","S_SFLASH_R0","Fixed","128","SORT","R – all LCS\nW – SORT","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["FACTORY_HASH_LIST","List of assets included into FACTORY_HASH (4-byte counter + 15*8-byte pairs + 4-byte checksum)","S_SFLASH_R0","Fixed","128","PROV","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["SECURE_HASH_LIST","List of assets included into SECURE_HASH (4-byte counter + 25*8-byte pairs + 4-byte checksum)","S_SFLASH_R0","Fixed","208","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["ASSET_HASH","Hash of assets provisioned up until SORT LCS (64-byte + 4-byte checksum)","OTP_ROT_BOOT","Fixed","68","SORT","R – all LCS\nW – SORT","Integrity (checksum verified by BOOT Firmware)","No"],
    ["FACTORY_HASH","Hash of assets provisioned up until PROVISIONED LCS (64-byte + 4-byte checksum)","OTP_ROT_BOOT","Fixed","68","PROV","R – all LCS\nW – PROV","Integrity (checksum verified by BOOT Firmware)","No"],
    ["SECURE_HASH","Hash of assets provisioned in factory and updated in the field. (64-byte + 4-byte checksum)","S_SFLASH_R0","Fixed","68","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","No"],
    ["OEM_POLICY_HASH","Separate hash of OEM_POLICY provisioned in factory and updated in the field. Used during Warm Boot. (64-byte + 4-byte checksum)","S_SFLASH_R0","Fixed","68","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","No"],
    ["RAM_APP_NV_CNT","Anti-rollback counter for RAM Applications updates (up to 64). (8-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","12","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["RAM_APP_NV_CNT_BKP","This backup is used by Tearing-safe write scheme for updating the counter. It includes 8-byte counter value + 4-byte checksum.","S_SFLASH_R0","Fixed","12 (+TS overhead)","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["RMA_TRIAL_CNT","This counter is used by TO_RMA RAM Application to count number of tries for erasing Manufacturer secrets and RT_SERVICES when the device transitions to RMA LCS. (4-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","8","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["RMA_TRIAL_CNT_BKP","This backup is used by Tearing-safe write scheme for updating the counter. It includes 4-byte counter value + 4-byte checksum.","S_SFLASH_R0","Fixed","8 (+TS overhead)","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["IFX_RMA_MASTER_KEY0","ECC public key is used for verifying signature of OpenRMA token. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_RMA_MASTER_KEY1","The second ECC public key is used if the first key (IFX_RMA_MASTER_KEY0) is revoked. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_RMA_MASTER_KEY_REVOC","Revocation flag is used for revoking the first key (IFX_RMA_MASTER_KEY0) if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (composite hash, checksum verified by BOOT Firmware)","Yes"],
    ["IFX_RMA_MASTER_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["IFX_APP_INTEGRITY_KEY0","First ECC public key used for verifying signature of Infineon application images. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_APP_INTEGRITY_KEY1","Second ECC public key used for verifying signature of Infineon application images. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["IFX_APP_INTEGRITY_KEY_REVOC","IFX_APP_INTEGRITY_KEY Revocation flag is used for revoking the first key if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["IFX_APP_INTEGRITY_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["IFX_APP_ENCRYPTION_KEY0","First key for encryption/decryption of Infineon application images. Stored obfuscated in 3 shares for PSC3+ devices. (32-byte*3 Shares + 2-byte key_type + 2-byte key_bits + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","104","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware) and Confidentiality","No"],
    ["IFX_APP_ENCRYPTION_KEY1","Second key for encryption/decryption of Infineon application images. Stored obfuscated in 3 shares. (32-byte*3 Shares + 2-byte key_type + 2-byte key_bits + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","104","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware) and Confidentiality","No"],
    ["IFX_APP_ENCRYPTION_KEY_REVOC","IFX_APP_ENCRYPTION_KEY Revocation flag is used for revoking the first key if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (composite hash, checksum verified by BOOT Firmware)","Yes"],
    ["IFX_APP_ENCRYPTION_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["IFX_REVOCATION_KEY","One ECC public key used for authenticating the key revocation message (certificate). (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by RAM Application)","No"],
    ["IFX_POLICY","Infineon manufacturer policy, for content definition refer to Section 5.1.4. (includes checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Product specific","PROV","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["PROTECTED_NVM_LOCKABLE","Deprecated - shall not be used if the product implements IFX_POLICY. For locking regions in PROTECTED_NVM. (8-bit lockable size + 8-bit redundancy + 12-bit for 4-byte alignment + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","8","SORT","R – all LCS\nW – PROV","Integrity (checksum verified by BOOT Firmware)","No"],
    ["NEXT_BOOT_IMAGE","NEXT_BOOT_IMAGE is the SW layer launched by RRAM_BOOT/FLASH_BOOT. Its integrity is checked and it is launched by RRAM_BOOT/FLASH_BOOT.","MAIN_NVM_R0","Custom - code image format","Product specific","SORT","R – all LCS\nW – NORMAL_P","Integrity (hash verified by BOOT Firmware)","No"],
    ["NEXT_BOOT_IMAGE_HASH","Reference Hash of NEXT_BOOT_IMAGE image. (64-byte + 4-byte checksum)","S_SFLASH_R0","Fixed","68","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (checksum verified by BOOT Firmware)","No"],
    ["NEXT_BOOT_IMAGE_NV_CNT","Anti-rollback counter for NEXT_BOOT_IMAGE updates. (8-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","12","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["NEXT_BOOT_IMAGE_NV_CNT_BKP","This backup is used by Tearing-safe write scheme for updating the counter. It includes 8-byte counter value + 4-byte checksum.","S_SFLASH_R0","Fixed","12 (+TS overhead)","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["OEM_ROT_KEY0_PROD","ECDSA Production OEM RoT public keys. Stored twice (duplicated) on non-M0SECCPUSS products. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT, OTP_ROT_SHARED\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["OEM_ROT_KEY1_PROD","The second ECDSA Production OEM RoT public key used if OEM_ROT_KEY0_PROD is revoked. Stored twice on non-M0SECCPUSS products. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT, OTP_ROT_SHARED\n[MXS40Sv2]: S_SFLASH_R0","Fixed","140","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["OEM_ROT_KEY_REVOC","OEM RoT Public Key Revocation flag is used for revoking the first key if compromised. Stored twice on non-M0SECCPUSS products.","[MXS22]: OTP_ROT_BOOT, OTP_ROT_SHARED\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Design dependent","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["OEM_ROT_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["OEM_ROT_KEY_DEV","ECDSA Development OEM RoT Public Key (136-byte + 4-byte checksum). Used in NORMAL_PROVISIONED LCS for development. Key is erased when transitioning to SECURE LCS.","S_SFLASH_R0","Fixed","140","NORMAL_P","R – NORMAL_P\nW – NORMAL_P","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["REPROV_POLICY_PROD","Production REPROVISIONING_POLICY determines if re-provisioning is allowed for keys, policies, chain-of-trust certificates. (includes checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by RAM Application)","Yes"],
    ["REPROV_POLICY_DEV","Development REPROVISIONING_POLICY determines if re-provisioning is allowed for keys, policies, chain-of-trust certificates. (includes checksum)","S_SFLASH_R0","Fixed","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P","Integrity (composite hash, checksum verified by RAM Application)","No"],
    ["REPROV_POLICY_PROD_BKP","This backup is used for Tearing-safety while updating the REPROV_POLICY_PROD (includes checksum).","S_SFLASH_R0","Fixed","Design dependent","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["RECOVERY_AGENT","RECOVERY_AGENT is the SW component launched by RRAM_BOOT/FLASH_BOOT in case of Secure-Boot or field update failure.","MAIN_NVM_R0","Custom - code image format","Product specific","SORT","R – all LCS\nW – NORMAL_P","Integrity (hash verified by BOOT Firmware)","No"],
    ["RECOVERY_AGENT_HASH","Hash of RECOVERY_AGENT image. (64-byte + 4-byte checksum)","S_SFLASH_R0","Fixed","68","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","No"],
    ["RECOVERY_AGENT_NV_CNT","Anti-rollback counter for RECOVERY_AGENT updates. (8-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: S_SFLASH_R0","Fixed","12","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["RECOVERY_AGENT_NV_CNT_BKP","This backup is used by Tearing-safe write scheme for updating the counter. It includes 8-byte counter value + 4-byte checksum.","S_SFLASH_R0","Fixed","12 (+TS overhead)","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["OEM_POLICY","OEM policy, part of OEM provisioning, for content definition refer to Section 5.1.4. (includes checksum)","S_SFLASH_R0","Fixed","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (composite hash, checksum verified by BOOT Firmware)","No"],
    ["OEM_POLICY_PUBLIC","Copy of OEM_POLICY accessible to bootloader. (includes checksum)","MAIN_NVM_R0","Fixed","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (composite hash)","No"],
    ["UPGRADE_FLAGS","Area for L1 and L2 FW to store flags which must survive device reset. (includes 4-byte checksum)","MAIN_NVM_R1","Fixed","5 (+ TS overhead)","SORT","R – all LCS\nW – NORMAL_P, SECURE","Integrity (checksum verified by L1/L2 FW)","Yes"],
    ["[Optional] HUK","HUK (Hardware Unique Key) is a device symmetric root key for deriving all device-specific keys. Stored obfuscated in 3 shares for PSC3+ devices. (32-byte*3 Shares + 2-byte key_type + 2-byte key_bits + 4-byte checksum). HUK becomes mandatory for PSC4 devices.","[MXS22]: OTP_ROT_SHARED\n[MXS40Sv2]: S_SFLASH_R0","Fixed. [MXS22]: Location in RRAM/SFLASH is HW defined","104","SORT","R – SORT, NORMAL_P, SECURE\nW – SORT, RMA","Integrity (composite hash, checksum verified by RAM Application) and Confidentiality","No"],
    ["[Optional] OEM_KEYS","OEM Application Keys for products without RT_SERVICES. Accessible to OEM SW. Opaque to BOOT Firmware. Asset writing by PROVISION_OEM RAM Application; reading fully managed by OEM SW.","MAIN_NVM_R0","Custom - see Description","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (composite hash, checksum verified by OEM SW)","No"],
    ["[RT_SERVICES] RT_SERVICES","RT_SERVICES are field upgradeable. Should be placed in area reclaimable as user memory space.","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Custom - code image format","128K","SORT","R – all LCS\nW – SORT, PROV, NORMAL_P, SECURE","Integrity (hash verified by BOOT Firmware)","see (1)"],
    ["[RT_SERVICES] RT_SERVICES_HASH","Hash of RT_SERVICES (64-byte + 4-byte checksum)","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Fixed","68","SORT","R – all LCS\nW – SORT, PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","see (1)"],
    ["[RT_SERVICES] RT_SERVICES_BASE","RT_SERVICES_BASE is locked in factory.","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Custom - code image format","28K","SORT","R – all LCS\nW – SORT","Integrity (hash verified by BOOT Firmware)","No"],
    ["[RT_SERVICES] RT_SERVICES_BASE_HASH","Hash of RT_SERVICES_BASE. Used to validate RT_SERVICES_BASE image before loading it. (64-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","68","SORT","R – all LCS\nW – SORT","Integrity (checksum verified by BOOT Firmware)","No"],
    ["[RT_SERVICES] IFX_RTS_NV_CNT","Anti-rollback counter for RT_SERVICES update (up to 128). Also used to determine which key to use for decryption. (16-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","20","SORT","R – all LCS\nW – SORT, PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["[RT_SERVICES] IFX_RTS_NV_CNT_BKP","This backup is used by Tearing-safe write scheme for updating the counter. It includes 16-byte counter value + 4-byte checksum.","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Fixed","20 (+TS overhead)","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["[RT_SERVICES] IFX_RTS_INTEGRITY_KEY0","First ECC public key used for authenticating the RT_SERVICES update image. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (checksum verified by RAM Application)","No"],
    ["[RT_SERVICES] IFX_RTS_INTEGRITY_KEY1","Second ECC public key used for authenticating the RT_SERVICES update image. (136-byte + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","140","SORT","R – all LCS\nW – PROV","Integrity (checksum verified by RAM Application)","No"],
    ["[RT_SERVICES] IFX_RTS_ENCR_KEY0","First RT_SERVICES update image symmetric encryption key. Stored obfuscated in 3 shares for PSC3+ devices. (32-byte*3 Shares + 2-byte key_type + 2-byte key_bits + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","104","SORT","R – PC0 only\nW – PROV","Integrity (checksum verified by RAM Application) and Confidentiality","No"],
    ["[RT_SERVICES] IFX_RTS_ENCR_KEY1","Second RT_SERVICES update image symmetric encryption key. Stored obfuscated in 3 shares for PSC3+ devices. (32-byte*3 Shares + 2-byte key_type + 2-byte key_bits + 4-byte checksum)","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","104","SORT","R – PC0 only\nW – PROV","Integrity (checksum verified by RAM Application) and Confidentiality","No"],
    ["[RT_SERVICES] IFX_RTS_INTEGRITY_KEY_REVOC","Revocation flag is used for revoking the first key if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["[RT_SERVICES] IFX_RTS_ENCR_KEY_REVOC","Revocation flag is used for revoking the first key if compromised.","[MXS22]: OTP_ROT_BOOT\n[MXS40Sv2]: N/A","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by BOOT Firmware)","Yes"],
    ["[RT_SERVICES] IFX_RTS_INTEGRITY_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["[RT_SERVICES] IFX_RTS_ENCR_KEY_REVOC_BKP","This backup is used for Tearing-safety while updating the revocation flag (includes checksum).","[MXS22]: S_SFLASH_R0\n[MXS40Sv2]: N/A","Fixed","Design dependent","SORT","R – all LCS\nW – PROV, NORMAL_P, SECURE","Integrity (checksum verified by RAM Application)","Yes"],
    ["[RT_SERVICES] RTS_IFX_KEYS","Additional Infineon Keys (e.g. WIFI or BT subsystem images encryption and authentication keys). Part of Infineon provisioning. Opaque to BOOT Firmware.","S_SFLASH_R0","Custom - see Description","Product specific","PROV","R – all LCS\nW – PROV","Integrity (composite hash, checksum verified by RT_SERVICES)","No"],
    ["[RT_SERVICES] RTS_OEM_KEYS","OEM Application Keys, part of OEM provisioning. Opaque to BOOT Firmware. Asset writing by PROVISION_OEM RAM Application; reading fully managed by RT_SERVICES.","S_SFLASH_R0","Custom - see Description","Product specific","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","Integrity (composite hash, checksum verified by RT_SERVICES)","No"],
    ["[RT_SERVICES] RT_SERVICES_OTP_AREA","Area for RT_SERVICES OTP assets. Contains assets such as OEM_NV_CNT. Asset reading/writing fully managed by RT_SERVICES.","[MXS22]: OTP_ROT_RT\n[MXS40Sv2]: n/a (use S_SFLASH_R1)","Custom - see Description","Product specific (4K typical)","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","No","No"],
    ["[RT_SERVICES] RT_SERVICES_WORK_AREA","Working area for RT_SERVICES. Contains RT_SERVICES initialization status, tearing safe backup for OEM_NV_CNT, keys created/imported during runtime, etc. NVM allocated cannot be reclaimed as user memory.","S_SFLASH_R1","Custom - see Description","Product specific (4K typical)","NORMAL_P","R – all LCS\nW – NORMAL_P, SECURE","No","No"],
]

# ── Styles ──────────────────────────────────────────────────────────────────
header_font  = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
header_fill  = PatternFill("solid", fgColor="1F4E79")
header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

cell_font    = Font(name="Calibri", size=10)
cell_align   = Alignment(vertical="top", wrap_text=True)

alt_fill     = PatternFill("solid", fgColor="D9E1F2")
white_fill   = PatternFill("solid", fgColor="FFFFFF")
opt_fill     = PatternFill("solid", fgColor="E2EFDA")   # green for Optional
rts_fill     = PatternFill("solid", fgColor="FFF2CC")   # yellow for RT_SERVICES

thin   = Side(style="thin", color="B0B0B0")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

# ── Write header ─────────────────────────────────────────────────────────────
for col_idx, h in enumerate(headers, start=1):
    c = ws.cell(row=1, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = header_align
    c.border = border

# ── Write data ────────────────────────────────────────────────────────────────
for row_idx, row_data in enumerate(data, start=2):
    asset_name = str(row_data[0])
    if "[Optional]" in asset_name:
        fill = opt_fill
    elif "[RT_SERVICES]" in asset_name:
        fill = rts_fill
    else:
        fill = alt_fill if row_idx % 2 == 0 else white_fill

    for col_idx, value in enumerate(row_data, start=1):
        c = ws.cell(row=row_idx, column=col_idx, value=value)
        c.font = cell_font
        c.alignment = cell_align
        c.fill = fill
        c.border = border

# ── Column widths ─────────────────────────────────────────────────────────────
col_widths = [35, 65, 35, 22, 15, 22, 35, 50, 10]
for i, w in enumerate(col_widths, start=1):
    ws.column_dimensions[get_column_letter(i)].width = w

# ── Row heights ───────────────────────────────────────────────────────────────
ws.row_dimensions[1].height = 30
for r in range(2, len(data) + 2):
    ws.row_dimensions[r].height = 55

# ── Freeze header ─────────────────────────────────────────────────────────────
ws.freeze_panes = "A2"

# ── Auto filter ───────────────────────────────────────────────────────────────
ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"

# ── Save ──────────────────────────────────────────────────────────────────────
wb.save("assets_table.xlsx")
print("assets_table.xlsx created successfully!")