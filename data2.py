from database import session, Translation

def print_translations():
    translations = session.query(Translation).all()
    for translation in translations:
        print(f"ID: {translation.id}")
        print(f"Source Text: {translation.source_text}")
        print(f"Translated Text: {translation.translated_text}")
        print(f"Source Language: {translation.source_language}")
        print(f"Target Language: {translation.target_language}")
        print(f"Timestamp: {translation.timestamp}")
        print("-" * 20)

if __name__ == '__main__':
    print_translations()
