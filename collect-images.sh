#!/bin/sh
# Copies the images actually referenced by the posts out of the Joomla
# images/ tree into static/images/ under web-safe names.
#
# Joomla accumulated years of renames, so some database references point at
# files that no longer exist. Those are reported at the end rather than
# aborting the run; anything findable by basename is recovered.
#
# Usage: sh collect-images.sh /path/to/extracted/images

SRC="${1:?usage: collect-images.sh <extracted images dir>}"
[ -d "$SRC" ] || { echo "not a directory: $SRC" >&2; exit 1; }
: > missing-images.txt
MISSING=0
RECOVERED=0

copy() {
  dest="static/images/$2"
  if [ -f "$SRC/$1" ]; then
    mkdir -p "$(dirname "$dest")" && cp "$SRC/$1" "$dest"
    return
  fi
  hit=$(find "$SRC" -type f -iname "$(basename "$1")" 2>/dev/null | head -1)
  if [ -n "$hit" ]; then
    mkdir -p "$(dirname "$dest")" && cp "$hit" "$dest"
    echo "  recovered: $1"
    RECOVERED=$((RECOVERED+1))
    return
  fi
  echo "$1" >> missing-images.txt
  MISSING=$((MISSING+1))
}

copy 2023/10/17/boy-resigned.png 2023/10/17/boy-resigned.png
copy 2023/10/17/boy-resigned1.png 2023/10/17/boy-resigned1.png
copy 2023/10/17/child-determined.png 2023/10/17/child-determined.png
copy 2023/10/18/resilient1.png 2023/10/18/resilient1.png
copy 2023/10/20/brave_I9g9bMev4C.png 2023/10/20/brave_i9g9bmev4c.png
copy 2023/10/21/brave_uHdy4St2Ra.jpg 2023/10/21/brave_uhdy4st2ra.jpg
copy 2023/10/30/brave_2Z9p3yJl2v.jpg 2023/10/30/brave_2z9p3yjl2v.jpg
copy 2023/11/06/wealth_of_subconscious.png 2023/11/06/wealth_of_subconscious.png
copy 2023/11/10/brave_CeEpA3a5MA.jpg 2023/11/10/brave_ceepa3a5ma.jpg
copy 2023/11/13/brave_RA7MdJZpd9.png 2023/11/13/brave_ra7mdjzpd9.png
copy 2023/11/14/FAILURE1.png 2023/11/14/failure1.png
copy 2023/12/05/PXL_20231128_202116464.jpg 2023/12/05/pxl_20231128_202116464.jpg
copy '2023/12/06/lightbulb - DALL·E 2023-12-05 21.33.47 - An oil painting style, dreamy image featuring a lightbulb with a large '"'"'10'"'"' in the middle. The image should convey a sense of wisdom and introspection.png' 2023/12/06/lightbulb-dall-e-2023-12-05-21.33.47-an-oil-painting-style-dreamy-image-featuring-a-lightbulb-with-a-large-10-in-the-middle.-the-image-should-convey-a-sense-of-wisdom-and-introspection.png
copy 2024/02/26/typing-fast.gif 2024/02/26/typing-fast.gif
copy 2024/05/03/PXL_20240503_130927840.jpg 2024/05/03/pxl_20240503_130927840.jpg
copy '2024/05/30/no pressure no diamonds.jpg' 2024/05/30/no-pressure-no-diamonds.jpg
copy 2024/06/03/10000064181.jpg 2024/06/03/10000064181.jpg
copy 2024/06/03/Tripartite-products.png 2024/06/03/tripartite-products.png
copy 2024/06/06/PXL_20240606_190018805.jpg 2024/06/06/pxl_20240606_190018805.jpg
copy 2024/06/09/PXL_20240608_021311283.jpg 2024/06/09/pxl_20240608_021311283.jpg
copy 2024/06/09/PXL_20240608_0213112831.jpg 2024/06/09/pxl_20240608_0213112831.jpg
copy 2024/06/09/PXL_20240608_021332761.MP.jpg 2024/06/09/pxl_20240608_021332761.mp.jpg
copy '2024/06/11/Color Hunt Palette 07133737b5b6b180f0f7bb7f.png' 2024/06/11/color-hunt-palette-07133737b5b6b180f0f7bb7f.png
copy '2024/06/11/Color Hunt Palette f8f8f8b180f037b5b62222221.png' 2024/06/11/color-hunt-palette-f8f8f8b180f037b5b62222221.png
copy 2024/06/18/448405506_10159837793525233_4638060454194643277_n.jpg 2024/06/18/448405506_10159837793525233_4638060454194643277_n.jpg
copy 2024/06/18/448405506_10159837793525233_4638060454194643277_n1.jpg 2024/06/18/448405506_10159837793525233_4638060454194643277_n1.jpg
copy 2024/06/18/IMG_20240618_135843.jpg 2024/06/18/img_20240618_135843.jpg
copy '2024/07/08/DALL·E 2024-07-08 12.35.46 - A colorful oil painting of a modern-looking man sitting at a sleek desk in a contemporary office, writing in a simple journal. The man is casually dre.webp' 2024/07/08/dall-e-2024-07-08-12.35.46-a-colorful-oil-painting-of-a-modern-looking-man-sitting-at-a-sleek-desk-in-a-contemporary-office-writing-in-a-simple-journal.-the-man-is-casually-dre.webp
copy '2024/08/26/product roadmap.png' 2024/08/26/product-roadmap.png
copy 2024/10/25/20240529_143941.jpg 2024/10/25/20240529_143941.jpg
copy 2024/11/15/SumatraPDF_cVZA6P2Y3F1.png 2024/11/15/sumatrapdf_cvza6p2y3f1.png
copy 2024/11/26/disjointed.png 2024/11/26/disjointed.png
copy 2025/01/02/PXL_20250102_022908726.jpg 2025/01/02/pxl_20250102_022908726.jpg
copy '2025/01/10/odonnel space station1.jpg' 2025/01/10/odonnel-space-station1.jpg
copy '2025/02/18/PXL_20250218_115840519~2.jpg' 2025/02/18/pxl_20250218_115840519-2.jpg
copy 2025/03/19/1000010712.jpg 2025/03/19/1000010712.jpg
copy 2025/03/19/1000010713.jpg 2025/03/19/1000010713.jpg
copy 2025/03/19/1000010714.jpg 2025/03/19/1000010714.jpg
copy 2025/03/19/1000010716.jpg 2025/03/19/1000010716.jpg
copy 2025/03/19/1000010717.jpg 2025/03/19/1000010717.jpg
copy 2025/05/19/make-decisions.png 2025/05/19/make-decisions.png
copy '2025/05/22/PXL_20250218_115840519~2 (1).jpg' 2025/05/22/pxl_20250218_115840519-2-1.jpg
copy 2025/06/03/Rose_Blumkin.jpg 2025/06/03/rose_blumkin.jpg
copy '2025/06/18/coding horror.png' 2025/06/18/coding-horror.png
copy 2025/08/25/1000012374.jpg 2025/08/25/1000012374.jpg
copy 2025/08/25/Anderson_Kane_904-2136-Heroic-jimstonephoto.com.png 2025/08/25/anderson_kane_904-2136-heroic-jimstonephoto.com.png
copy 2025/09/15/outlive.jpg 2025/09/15/outlive.jpg
copy 2025/09/22/inspired-product-development-cycle.jpg 2025/09/22/inspired-product-development-cycle.jpg
copy 2025/09/22/inspired.jpg 2025/09/22/inspired.jpg
copy 2025/12/22/PXL_20251222_174633485.jpg 2025/12/22/pxl_20251222_174633485.jpg
copy 2025/12/22/PXL_20251222_174958777.jpg 2025/12/22/pxl_20251222_174958777.jpg
copy 2026/01/02/Carousel-1-image-1.png 2026/01/02/carousel-1-image-1.png
copy 2026/01/02/Carousel-1-image-2.png 2026/01/02/carousel-1-image-2.png
copy 2026/01/02/Carousel-1-image-3.png 2026/01/02/carousel-1-image-3.png
copy 2026/01/02/Carousel-1-image-4.png 2026/01/02/carousel-1-image-4.png
copy 2026/01/02/Carousel-1-image-5.png 2026/01/02/carousel-1-image-5.png
copy 2026/01/02/kane-anderson-HGAD-QR-Code.jpg 2026/01/02/kane-anderson-hgad-qr-code.jpg
copy '2026/03/31/A_programmer_late_at_night_(see_image)_using_an_ai_chatbot_and_drinking_coffee._he_types_and_changes_seed2466868342 (1).gif' 2026/03/31/a_programmer_late_at_night_-see_image-_using_an_ai_chatbot_and_drinking_coffee._he_types_and_changes_seed2466868342-1.gif
copy '2026/04/08/oil painting of a leader planting a flag at a stony summit, with people supporting him..jpg' 2026/04/08/oil-painting-of-a-leader-planting-a-flag-at-a-stony-summit-with-people-supporting-him..jpg
copy Lightsail-console.png lightsail-console.png
copy 'MicrosoftTeams-image 75.png' microsoftteams-image-75.png
copy courage-connection.png courage-connection.png
copy dunning-kruger.MP2.jpg dunning-kruger.mp2.jpg
copy godaddy-dns-record.png godaddy-dns-record.png
copy image-20260310-043312.png image-20260310-043312.png
copy image-20260310-043535.png image-20260310-043535.png
copy lightsail-static-ip.png lightsail-static-ip.png

echo "collected 68 references: $(((68 - MISSING))) present, $RECOVERED recovered by search, $MISSING missing"
[ "$MISSING" -gt 0 ] && echo "see missing-images.txt" || rm -f missing-images.txt
exit 0
