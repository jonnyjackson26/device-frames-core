from pathlib import Path

from device_frames_core import list_devices, find_template, get_frame_image, get_mask_image, apply_frame

# Test list_devices
print("=== Testing list_devices ===")
all_devices = list_devices()
print(f"Total devices: {len(all_devices)}")

ios_devices = list_devices(category="ios")
print(f"iOS devices: {len(ios_devices)}")

iphone_16_pro_max = list_devices(category="ios", device="16-pro-max")
print(f"iPhone 16 Pro Max variations: {len(iphone_16_pro_max)}")
for variation in iphone_16_pro_max:
    print(f"  - {variation['variation']}")

# Test find_template
print("\n=== Testing find_template ===")
template = find_template(device="16-pro-max", variation="black-titanium", category="ios")
print(template)

# Test get_frame_image
print("\n=== Testing get_frame_image ===")
frame = get_frame_image(device="16-pro-max", variation="black-titanium", category="ios")
print(f"Frame image size: {frame.size}")
print(f"Frame image mode: {frame.mode}")

# Test get_mask_image
print("\n=== Testing get_mask_image ===")
mask = get_mask_image(device="16-pro-max", variation="black-titanium", category="ios")
print(f"Mask image size: {mask.size}")
print(f"Mask image mode: {mask.mode}")

# Test error handling
print("\n=== Testing error handling ===")
try:
    list_devices(device="16-pro-max")  # Should fail - no category
except ValueError as e:
    print(f"✓ Caught expected error: {e}")

# Test apply_frame
print("\n=== Testing apply_frame ===")
output = apply_frame(
    screenshot_path=Path("tests/iphone.PNG"),
    device="16-pro-max",
    variation="black-titanium",
    output_path=Path("tests/iphone_framed.png"),
    category="ios",
)
print(f"✓ Frame applied successfully")
print(f"Output: {output}")