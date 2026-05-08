import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List

from obfuscator import process_obfuscate
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, x25519


KEY_TYPES = [
	"ECDSA-P256",
	"ECDSA-P384",
	"ECDSA-P521",
	"X25519",
	"RSA2048",
	"RSA3072",
	"RSA4096",
	"AES128",
	"AES192",
	"AES256",
]

ASYMMETRIC_KEY_TYPES = [
	"ECDSA-P256",
	"ECDSA-P384",
	"ECDSA-P521",
	"X25519",
	"RSA2048",
	"RSA3072",
	"RSA4096",
]

SYMMETRIC_KEY_TYPES = [
	"AES128",
	"AES192",
	"AES256",
]


def parse_key_list_file(file_path: str) -> List[str]:
	keys: List[str] = []

	with open(file_path, "r", encoding="utf-8") as key_file:
		for raw_line in key_file:
			line = raw_line.strip()
			if not line:
				continue

			line = re.sub(r"\(.*?\)", "", line).strip()
			line = line.rstrip(",").strip()
			if line:
				keys.append(line)

	return keys


def generate_private_key_bytes(key_type: str) -> bytes:
	if key_type == "ECDSA-P256":
		key = ec.generate_private_key(ec.SECP256R1())
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "ECDSA-P384":
		key = ec.generate_private_key(ec.SECP384R1())
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "ECDSA-P521":
		key = ec.generate_private_key(ec.SECP521R1())
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "X25519":
		key = x25519.X25519PrivateKey.generate()
		return key.private_bytes(
			encoding=serialization.Encoding.Raw,
			format=serialization.PrivateFormat.Raw,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "RSA2048":
		key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "RSA3072":
		key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "RSA4096":
		key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
		return key.private_bytes(
			encoding=serialization.Encoding.PEM,
			format=serialization.PrivateFormat.PKCS8,
			encryption_algorithm=serialization.NoEncryption(),
		)

	if key_type == "AES128":
		return os.urandom(16)

	if key_type == "AES192":
		return os.urandom(24)

	if key_type == "AES256":
		return os.urandom(32)

	raise ValueError(f"Unsupported key type: {key_type}")


def is_asymmetric_key_type(key_type: str) -> bool:
	return key_type in {
		"ECDSA-P256",
		"ECDSA-P384",
		"ECDSA-P521",
		"X25519",
		"RSA2048",
		"RSA3072",
		"RSA4096",
	}


def is_symmetric_key_type(key_type: str) -> bool:
	return key_type in set(SYMMETRIC_KEY_TYPES)


def generate_asymmetric_private_key(key_type: str):
	if key_type == "ECDSA-P256":
		return ec.generate_private_key(ec.SECP256R1())

	if key_type == "ECDSA-P384":
		return ec.generate_private_key(ec.SECP384R1())

	if key_type == "ECDSA-P521":
		return ec.generate_private_key(ec.SECP521R1())

	if key_type == "X25519":
		return x25519.X25519PrivateKey.generate()

	if key_type == "RSA2048":
		return rsa.generate_private_key(public_exponent=65537, key_size=2048)

	if key_type == "RSA3072":
		return rsa.generate_private_key(public_exponent=65537, key_size=3072)

	if key_type == "RSA4096":
		return rsa.generate_private_key(public_exponent=65537, key_size=4096)

	raise ValueError(f"Unsupported asymmetric key type: {key_type}")


def serialize_asymmetric_key_pair(private_key, encoding: serialization.Encoding) -> tuple[bytes, bytes]:
	private_bytes = private_key.private_bytes(
		encoding=encoding,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption(),
	)
	public_bytes = private_key.public_key().public_bytes(
		encoding=encoding,
		format=serialization.PublicFormat.SubjectPublicKeyInfo,
	)
	return private_bytes, public_bytes


def to_hex_text(data: bytes) -> str:
	return "\n".join(data.hex()[i:i + 64] for i in range(0, len(data.hex()), 64)) + "\n"


def to_c_array_source(var_name: str, data: bytes) -> str:
	bytes_per_line = 4
	byte_literals = [f"0x{value:02X}" for value in data]
	lines = [
		", ".join(byte_literals[i:i + bytes_per_line])
		for i in range(0, len(byte_literals), bytes_per_line)
	]
	body = "\n".join(f"    {line}," for line in lines)

	return (
		"#include <stdint.h>\n"
		"#include <stddef.h>\n\n"
		f"const uint8_t {var_name}[] = {{\n"
		f"{body}\n"
		"};\n\n"
		f"const size_t {var_name}_len = sizeof({var_name});\n"
	)


def file_extension_for_key_type(key_type: str) -> str:
	if key_type in {"AES128", "AES192", "AES256", "X25519"}:
		return "bin"
	return "pem"


class KeyGenerationApp(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.title("Key Generation GUI")
		self.geometry("980x680")

		base_dir = os.path.dirname(os.path.abspath(__file__))
		self.key_list_path = os.path.join(base_dir, "key_lists.txt")
		self.output_folder_var = tk.StringVar(value=base_dir)

		self.key_name_vars: Dict[str, tk.BooleanVar] = {}
		self.key_type_vars: Dict[str, tk.BooleanVar] = {
			key_type: tk.BooleanVar(value=False) for key_type in KEY_TYPES
		}
		self.key_family_var = tk.StringVar(value="asymmetric")
		self.asymmetric_type_checkbuttons: List[ttk.Checkbutton] = []
		self.symmetric_type_checkbuttons: List[ttk.Checkbutton] = []
		self.symmetric_obfuscation_var = tk.BooleanVar(value=False)
		self.obf_option_cb: ttk.Checkbutton | None = None

		self._build_ui()
		self._load_key_names()

	def _build_ui(self) -> None:
		container = ttk.Frame(self, padding=12)
		container.pack(fill=tk.BOTH, expand=True)

		style = ttk.Style(self)
		style.configure("BottomBig.TButton", padding=(14, 10))

		header = ttk.Label(
			container,
			text="Key Generation Program",
			font=("Segoe UI", 14, "bold"),
		)
		header.pack(anchor="w", pady=(0, 8))

		folder_frame = ttk.LabelFrame(container, text="Select Output Folder", padding=8)
		folder_frame.pack(fill=tk.X, pady=(0, 10))

		folder_entry = ttk.Entry(folder_frame, textvariable=self.output_folder_var)
		folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

		browse_btn = ttk.Button(folder_frame, text="Folder Search", command=self._choose_folder)
		browse_btn.pack(side=tk.LEFT)

		selection_frame = ttk.Frame(container)
		selection_frame.pack(fill=tk.BOTH, expand=True)

		key_name_group = ttk.LabelFrame(
			selection_frame,
			text="Select Key Names (key_lists.txt)",
			padding=8,
		)
		key_name_group.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

		key_type_group = ttk.LabelFrame(
			selection_frame,
			text="Select Key Types (multiple)",
			padding=8,
		)
		key_type_group.pack(side=tk.RIGHT, fill=tk.Y)

		family_group = ttk.LabelFrame(key_type_group, text="Key Family", padding=6)
		family_group.pack(fill=tk.X, pady=(0, 8))

		asym_family_rb = ttk.Radiobutton(
			family_group,
			text="Asymmetric",
			value="asymmetric",
			variable=self.key_family_var,
			command=self._on_key_family_changed,
		)
		asym_family_rb.pack(anchor="w")

		sym_family_rb = ttk.Radiobutton(
			family_group,
			text="Symmetric",
			value="symmetric",
			variable=self.key_family_var,
			command=self._on_key_family_changed,
		)
		sym_family_rb.pack(anchor="w")

		self.canvas = tk.Canvas(key_name_group, highlightthickness=0)
		self.scrollbar = ttk.Scrollbar(key_name_group, orient="vertical", command=self.canvas.yview)
		self.scrollable_frame = ttk.Frame(self.canvas)

		self.scrollable_frame.bind(
			"<Configure>",
			lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
		)

		self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		self.canvas.configure(yscrollcommand=self.scrollbar.set)

		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

		asym_group = ttk.LabelFrame(key_type_group, text="Asymmetric (priv: pem / pub: pem, hex, c)", padding=6)
		asym_group.pack(fill=tk.X, pady=(0, 8))

		sym_group = ttk.LabelFrame(key_type_group, text="Symmetric (bin, hex)", padding=6)
		sym_group.pack(fill=tk.X)

		for key_type in ASYMMETRIC_KEY_TYPES:
			type_cb = ttk.Checkbutton(
				asym_group,
				text=key_type,
				variable=self.key_type_vars[key_type],
				command=self._update_obfuscation_option_state,
			)
			type_cb.pack(anchor="w", pady=1)
			self.asymmetric_type_checkbuttons.append(type_cb)

		for key_type in SYMMETRIC_KEY_TYPES:
			type_cb = ttk.Checkbutton(
				sym_group,
				text=key_type,
				variable=self.key_type_vars[key_type],
				command=self._update_obfuscation_option_state,
			)
			type_cb.pack(anchor="w", pady=1)
			self.symmetric_type_checkbuttons.append(type_cb)

		self.obf_option_cb = ttk.Checkbutton(
			key_type_group,
			text="Symmetric Obfuscation (km_:Key modifier obf:Obfusaction files)",
			variable=self.symmetric_obfuscation_var,
		)
		self.obf_option_cb.pack(anchor="w", pady=(8, 0))
		self._sync_key_type_controls_for_family()
		self._update_obfuscation_option_state()

		actions_frame = ttk.Frame(container)
		actions_frame.pack(fill=tk.X, pady=(10, 0))

		select_all_btn = ttk.Button(
			actions_frame,
			text="Select All Keys",
			command=self._select_all_keys,
			style="BottomBig.TButton",
		)
		select_all_btn.pack(side=tk.LEFT, padx=(0, 6))

		clear_all_btn = ttk.Button(
			actions_frame,
			text="Clear Key Selection",
			command=self._clear_all_keys,
			style="BottomBig.TButton",
		)
		clear_all_btn.pack(side=tk.LEFT, padx=(0, 12))

		select_all_types_btn = ttk.Button(
			actions_frame,
			text="Select All Types",
			command=self._select_all_types,
			style="BottomBig.TButton",
		)
		select_all_types_btn.pack(side=tk.LEFT, padx=(0, 6))

		clear_all_types_btn = ttk.Button(
			actions_frame,
			text="Clear Type Selection",
			command=self._clear_all_types,
			style="BottomBig.TButton",
		)
		clear_all_types_btn.pack(side=tk.LEFT, padx=(0, 12))

		generate_btn = ttk.Button(
			actions_frame,
			text="Generate Keys",
			command=self._generate_keys,
			style="BottomBig.TButton",
		)
		generate_btn.pack(side=tk.LEFT)

	def _load_key_names(self) -> None:
		if not os.path.exists(self.key_list_path):
			messagebox.showerror("Error", f"Cannot find key list file.\n{self.key_list_path}")
			return

		for widget in self.scrollable_frame.winfo_children():
			widget.destroy()

		key_names = parse_key_list_file(self.key_list_path)
		self.key_name_vars = {name: tk.BooleanVar(value=False) for name in key_names}

		for key_name in key_names:
			row = ttk.Frame(self.scrollable_frame)
			row.pack(fill=tk.X, pady=2)

			cb = ttk.Checkbutton(
				row,
				text=key_name,
				variable=self.key_name_vars[key_name],
			)
			cb.pack(side=tk.LEFT, anchor="w")

	def _choose_folder(self) -> None:
		folder = filedialog.askdirectory(title="Select Output Folder")
		if folder:
			self.output_folder_var.set(folder)

	def _select_all_keys(self) -> None:
		for var in self.key_name_vars.values():
			var.set(True)

	def _clear_all_keys(self) -> None:
		for var in self.key_name_vars.values():
			var.set(False)

	def _select_all_types(self) -> None:
		if self.key_family_var.get() == "symmetric":
			for key_type in SYMMETRIC_KEY_TYPES:
				self.key_type_vars[key_type].set(True)
		else:
			for key_type in ASYMMETRIC_KEY_TYPES:
				self.key_type_vars[key_type].set(True)
		self._update_obfuscation_option_state()

	def _clear_all_types(self) -> None:
		for var in self.key_type_vars.values():
			var.set(False)
		self._update_obfuscation_option_state()

	def _on_key_family_changed(self) -> None:
		self._sync_key_type_controls_for_family()
		self._update_obfuscation_option_state()

	def _sync_key_type_controls_for_family(self) -> None:
		selected_family = self.key_family_var.get()
		enable_symmetric = selected_family == "symmetric"

		for cb in self.symmetric_type_checkbuttons:
			cb.configure(state=tk.NORMAL if enable_symmetric else tk.DISABLED)
		if not enable_symmetric:
			for key_type in SYMMETRIC_KEY_TYPES:
				self.key_type_vars[key_type].set(False)

		for cb in self.asymmetric_type_checkbuttons:
			cb.configure(state=tk.DISABLED if enable_symmetric else tk.NORMAL)
		if enable_symmetric:
			for key_type in ASYMMETRIC_KEY_TYPES:
				self.key_type_vars[key_type].set(False)

	def _update_obfuscation_option_state(self) -> None:
		selected_family = self.key_family_var.get()
		has_symmetric_selected = any(
			self.key_type_vars[key_type].get() for key_type in SYMMETRIC_KEY_TYPES
		)
		can_enable_obfuscation = selected_family == "symmetric" and has_symmetric_selected

		if not can_enable_obfuscation:
			self.symmetric_obfuscation_var.set(False)

		if self.obf_option_cb is not None:
			state = tk.NORMAL if can_enable_obfuscation else tk.DISABLED
			self.obf_option_cb.configure(state=state)

	def _generate_keys(self) -> None:
		selected_family = self.key_family_var.get()
		selected_key_names = [
			key_name for key_name, var in self.key_name_vars.items() if var.get()
		]
		selected_key_types = [
			key_type for key_type, var in self.key_type_vars.items() if var.get()
		]

		if selected_family == "symmetric":
			selected_key_types = [
				key_type for key_type in selected_key_types if key_type in SYMMETRIC_KEY_TYPES
			]
		else:
			selected_key_types = [
				key_type for key_type in selected_key_types if key_type in ASYMMETRIC_KEY_TYPES
			]
		enable_symmetric_obfuscation = self.symmetric_obfuscation_var.get()

		output_folder = self.output_folder_var.get().strip()

		if not selected_key_names:
			messagebox.showwarning("Selection Required", "Please select at least one key name.")
			return

		if not selected_key_types:
			messagebox.showwarning("Selection Required", "Please select at least one key type.")
			return

		if not output_folder:
			messagebox.showwarning("Selection Required", "Please select an output folder.")
			return

		try:
			os.makedirs(output_folder, exist_ok=True)
		except OSError as exc:
			messagebox.showerror("Error", f"Failed to create folder: {exc}")
			return

		created_files: List[str] = []
		failed_items: List[str] = []

		for key_name in selected_key_names:
			safe_key_name = re.sub(r"[^a-zA-Z0-9._-]", "_", key_name)
			folder_key_name = safe_key_name.upper()
			file_key_name = safe_key_name.lower()

			key_folder = os.path.join(output_folder, folder_key_name)
			os.makedirs(key_folder, exist_ok=True)

			for key_type in selected_key_types:
				if key_type not in KEY_TYPES:
					failed_items.append(f"{key_name}: invalid key type ({key_type})")
					continue

				try:
					file_key_type = key_type.lower()

					if is_asymmetric_key_type(key_type):
						private_key = generate_asymmetric_private_key(key_type)

						pem_priv, pem_pub = serialize_asymmetric_key_pair(
							private_key,
							serialization.Encoding.PEM,
						)
						bin_priv, bin_pub = serialize_asymmetric_key_pair(
							private_key,
							serialization.Encoding.DER,
						)

						# Private key: only .pem
						private_pem_name = f"{file_key_name}_{file_key_type}_priv.pem"
						private_pem_path = os.path.join(key_folder, private_pem_name)
						with open(private_pem_path, "wb") as private_file:
							private_file.write(pem_priv)
						created_files.append(os.path.relpath(private_pem_path, output_folder))

						# Public key: .pem, .hex, .c
						public_pem_name = f"{file_key_name}_{file_key_type}_pub.pem"
						public_pem_path = os.path.join(key_folder, public_pem_name)
						with open(public_pem_path, "wb") as public_file:
							public_file.write(pem_pub)
						created_files.append(os.path.relpath(public_pem_path, output_folder))

						public_hex_name = f"{file_key_name}_{file_key_type}_pub_hex.txt"
						public_hex_path = os.path.join(key_folder, public_hex_name)
						with open(public_hex_path, "w", encoding="utf-8") as public_hex_file:
							public_hex_file.write(to_hex_text(bin_pub))
						created_files.append(os.path.relpath(public_hex_path, output_folder))

						base_symbol = re.sub(r"[^a-zA-Z0-9_]", "_", f"{file_key_name}_{file_key_type}")
						public_c_name = f"{file_key_name}_{file_key_type}_pub.c"
						public_c_path = os.path.join(key_folder, public_c_name)
						with open(public_c_path, "w", encoding="utf-8") as public_c_file:
							public_c_file.write(to_c_array_source(f"{base_symbol}_pub", bin_pub))
						created_files.append(os.path.relpath(public_c_path, output_folder))
					else:
						ext = file_extension_for_key_type(key_type)
						data = generate_private_key_bytes(key_type)
						output_name = f"{file_key_name}_{file_key_type}.{ext}"
						output_path = os.path.join(key_folder, output_name)

						with open(output_path, "wb") as out_file:
							out_file.write(data)
						created_files.append(os.path.relpath(output_path, output_folder))

						if is_symmetric_key_type(key_type):
							hex_name = f"{file_key_name}_{file_key_type}_hex.txt"
							hex_path = os.path.join(key_folder, hex_name)
							with open(hex_path, "w", encoding="utf-8") as hex_file:
								hex_file.write(to_hex_text(data))
							created_files.append(os.path.relpath(hex_path, output_folder))

							if enable_symmetric_obfuscation:
								key_modifier = os.urandom(32)

								km_name = f"km_{file_key_name}_{file_key_type}.{ext}"
								km_path = os.path.join(key_folder, km_name)
								with open(km_path, "wb") as km_file:
									km_file.write(key_modifier)
								created_files.append(os.path.relpath(km_path, output_folder))

								km_hex_name = f"km_{file_key_name}_{file_key_type}_hex.txt"
								km_hex_path = os.path.join(key_folder, km_hex_name)
								with open(km_hex_path, "w", encoding="utf-8") as km_hex_file:
									km_hex_file.write(to_hex_text(key_modifier))
								created_files.append(os.path.relpath(km_hex_path, output_folder))
				except Exception as exc:
					failed_items.append(f"{key_name} / {key_type}: {exc}")

		result_lines = [f"Number of files generated: {len(created_files)}"]
		if created_files:
			preview = "\n".join(created_files[:20])
			result_lines.append(f"\nGenerated files (up to 20):\n{preview}")

		if failed_items:
			fail_preview = "\n".join(failed_items[:10])
			result_lines.append(f"\nFailed items (up to 10):\n{fail_preview}")

		messagebox.showinfo("Result", "\n".join(result_lines))


if __name__ == "__main__":
	app = KeyGenerationApp()
	app.mainloop()
