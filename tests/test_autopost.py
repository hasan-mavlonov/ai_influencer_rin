from rin.agent import RinAgent
from rin.actions import generate_image_for_topic, create_post_entry
from rin.posting import post_to_instagram

def main():
    rin = RinAgent()
    topic = rin.generate_topic()
    caption = rin.generate_caption(topic)
    image_path = generate_image_for_topic(topic)
    post = create_post_entry(topic, caption, image_path)

    print(f"✅ Created new post:\nTopic: {post['topic']}\nCaption: {post['caption']}\nImage: {post['image_path']}")

    # Upload to Instagram
    print("📤 Uploading to Instagram...")
    post_to_instagram(post["image_path"], post["caption"])
    print("✅ Done!")


if __name__ == "__main__":
    main()
