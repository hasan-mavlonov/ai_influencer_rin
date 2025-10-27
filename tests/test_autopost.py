# tests/test_autopost.py
from rin.agent import RinAgent
from rin.actions import generate_image_for_topic, create_post_entry

rin = RinAgent()
topic = rin.generate_topic()
caption = rin.generate_caption(topic)
image_path = generate_image_for_topic(topic)
post = create_post_entry(topic, caption, image_path)

print(f"✅ Created new post:\nTopic: {post['topic']}\nCaption: {post['caption']}\nImage: {post['image_path']}")
