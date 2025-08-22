from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import os

def create_american_flag(size):
    """Create a simple American flag image of the given size."""
    width, height = size
    flag = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(flag)

    # Draw 13 stripes
    stripe_height = height // 13
    for i in range(13):
        if i % 2 == 0:
            y0 = i * stripe_height
            y1 = height if i == 12 else (i + 1) * stripe_height
            draw.rectangle([0, y0, width, y1], fill="red")

    # Draw blue canton
    canton_height = stripe_height * 7
    canton_width = int(width * 0.4)
    draw.rectangle([0, 0, canton_width, canton_height], fill="navy")

    # Draw white stars (5 rows of 6, 4 rows of 5)
    star_radius = max(1, min(canton_height // 20, canton_width // 20))
    for row in range(9):
        stars_in_row = 6 if row % 2 == 0 else 5
        y = int((row + 1) * canton_height / 10)
        for col in range(stars_in_row):
            x = int((col + 1) * canton_width / (stars_in_row + 1))
            draw.ellipse(
                [x - star_radius, y - star_radius, x + star_radius, y + star_radius],
                fill="white",
            )
    return flag

def apply_flag_background_filter(image_path, output_path="flag_background_image.png"):
    try:
        # Open and resize the original image
        img = Image.open(image_path).convert("RGBA")
        img_resized = img.resize((128, 128))

        # Create American flag the same size as the image
        flag_bg = create_american_flag(img_resized.size).convert("RGBA")

        # Make the flag semi-transparent (40% opacity)
        flag_bg.putalpha(int(255 * 0.4))

        # Overlay the flag on top of the original image
        result = Image.alpha_composite(img_resized, flag_bg)

        # Save result
        plt.imshow(result)
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Processed image saved as '{output_path}'.")

    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    print("Image American Flag Background Processor (type 'exit' to quit)\n")
    while True:
        image_path = input("Enter image filename (or 'exit' to quit): ").strip()
        if image_path.lower() == 'exit':
            print("Goodbye!")
            break
        if not os.path.isfile(image_path):
            print(f"File not found: {image_path}")
            continue
        base, ext = os.path.splitext(image_path)
        output_file = f"{base}_flag{ext}"
        apply_flag_background_filter(image_path, output_file)