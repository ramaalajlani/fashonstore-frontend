import cv2
import numpy as np
import matplotlib.pyplot as plt

def determine_skin_tone_lab(avg_lab):
    l, a, b = avg_lab  # استخراج قيم LAB

    # طباعة القيم لمساعدتنا في التصحيح
    print(f"قيم LAB: L={l}, A={a}, B={b}")

    # تصنيف درجة لون البشرة بناءً على فرق A و B
    if a > b + 5:  # إذا كانت قيمة الأحمر (A) أعلى بفارق عن الأصفر (B)
        return "دافئة 🔥"
    elif b > a + 5:  # إذا كانت قيمة الأصفر (B) أعلى بفارق عن الأحمر (A)
        return "باردة ❄️"
    else:  # إذا كانت القيم متقاربة
        return "معتدلة 🌿"

# تحميل الصورة
image_path = "C:\\Users\\LENOVO\\Desktop\\photo_2025-03-19_14-18-59.jpg"
image = cv2.imread(image_path)

if image is None:
    print("خطأ في تحميل الصورة. تأكد من المسار الصحيح.")
else:
    # تحويل الصورة من BGR إلى RGB ثم إلى LAB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_lab = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2LAB)

    # تحديد حدود لون البشرة في LAB
    lower_skin = np.array([0, 120, 125], dtype=np.uint8)
    upper_skin = np.array([255, 160, 170], dtype=np.uint8)

    # استخراج قناع للبشرة
    skin_mask = cv2.inRange(image_lab, lower_skin, upper_skin)

    # تطبيق القناع على الصورة الأصلية
    skin_segment = cv2.bitwise_and(image_lab, image_lab, mask=skin_mask)

    # استخراج قيم LAB من مناطق البشرة التي تم اكتشافها
    skin_pixels = image_lab[skin_mask > 0]

    if len(skin_pixels) > 0:
        # حساب متوسط اللون
        average_skin_color = np.mean(skin_pixels, axis=0).astype(int)

        # استخراج نتيجة التصنيف
        skin_tone = determine_skin_tone_lab(average_skin_color)

        # طباعة النتيجة
        print("درجة حرارة لون البشرة:", skin_tone)
    else:
        print("لم يتم العثور على مناطق للبشرة.")

    # عرض الصورة مع تحديد مناطق البشرة
    plt.imshow(cv2.cvtColor(skin_segment, cv2.COLOR_LAB2RGB))
    plt.axis("off")
    plt.title("المناطق التي تم تحديدها كلون البشرة")
    plt.show()