import discord
import json
from datetime import datetime

class scrapemes:
    def __init__(self, bot_token, channel_id):
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.messages = []
        
        intents = discord.Intents.default()
        intents.messages = True
        intents.guilds = True
        intents.message_content = True
        
        self.client = discord.Client(intents=intents)
        
        self.client.event(self.on_ready)
    
    async def on_ready(self):
        print(f'Bot connecté : {self.client.user}')
        channel = self.client.get_channel(self.channel_id)
        
        if not channel:
            print("not found channel id")
            await self.client.close()
            return
        
        print(f"getting message of channel : {channel.name}")
        
        try:
            async for message in channel.history(limit=None):
                self.save_message(message)
                
            self.save_to_file()
            
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            await self.client.close()
    
    def save_message(self, message):
        embed_data = []
        
        for embed in message.embeds:
            embed_info = {
                'title': embed.title,
                'description': embed.description,
                'url': embed.url,
                'fields': [],
                'footer': str(embed.footer) if embed.footer else None,
                'image': embed.image.url if embed.image else None,
                'thumbnail': embed.thumbnail.url if embed.thumbnail else None
            }
            
            if embed.fields:
                for field in embed.fields:
                    embed_info['fields'].append({
                        'name': field.name,
                        'value': field.value,
                        'inline': field.inline
                    })
            
            embed_data.append(embed_info)
        
        message_data = {
            'id': str(message.id),
            'author': str(message.author),
            'content': message.content,
            'timestamp': message.created_at.isoformat(),
            'attachments': [a.url for a in message.attachments],
            'embeds': embed_data
        }
        
        self.messages.append(message_data)
        print(f"messages saved : {message.author} - {message.content[:30]}...")
    
    def save_to_file(self):
        filename = f"discord_export_{self.channel_id}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=2)
        print(f"done {len(self.messages)} saved in {filename}")
    
    def run(self):
        self.client.run(self.bot_token)

if __name__ == "__main__":
    TOKEN = "YOUR BOT TOKEN HERE"
    CHANNEL_ID = CHANNELIDHERE
    scraper = scrapemes(TOKEN, CHANNEL_ID)
    scraper.run()