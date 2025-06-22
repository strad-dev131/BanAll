
# 🔥 Telegram Ban-All Bot - Ultra Powerful & Secure

The **most advanced Telegram group management bot** with lightning-fast performance, military-grade security, and enterprise-level reliability.

## 🎯 Features

### 🔒 **Ultra Secure**
- **Sudo-only access** - Only authorized users can execute commands
- **Admin protection** - Won't affect group admins or creators
- **Self-protection** - Bot cannot be banned by its own commands
- **Environment-based security** - All secrets stored securely

### ⚡ **Lightning Fast**
- **Asynchronous operations** - Process thousands of members simultaneously
- **Intelligent batching** - Optimized for large groups (10K+ members)
- **FloodWait handling** - Smart retry mechanism with exponential backoff
- **Progress tracking** - Real-time operation updates

### 🧠 **Smart & Reliable**
- **MongoDB logging** - Complete audit trail of all actions
- **Error resilience** - 100% uptime with comprehensive error handling
- **Performance optimization** - Configurable concurrent operations
- **24/7 stability** - Production-ready for VPS deployment

## 🚀 Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `/start` | Initialize bot and show welcome message | Sudo Only |
| `/help` | Display all available commands | Sudo Only |
| `/banall` | Ban all non-admin members | Sudo Only |
| `/unbanall` | Unban all banned members | Sudo Only |
| `/kickall` | Kick all non-admin members | Sudo Only |
| `/kickbots` | Remove all bots from group | Sudo Only |
| `/muteall` | Mute all non-admin members | Sudo Only |
| `/unmuteall` | Unmute all muted members | Sudo Only |
| `/stats` | Get group statistics | Sudo Only |
| `/logs` | View recent action logs | Sudo Only |

## 📋 Requirements

### System Requirements
- Python 3.11+
- MongoDB Atlas (Free tier supported)
- Telegram Bot Token
- Telegram API credentials

### Python Dependencies
```
pyrogram==2.0.106
TgCrypto==1.2.5
motor==3.3.2
python-dotenv==1.0.0
dnspython==2.4.2
```

## 🛠️ Installation & Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/strad-dev131/BanAll
cd BanAll
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment
1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` with your credentials:
```env
# Telegram API Configuration
API_ID=1234567
API_HASH=your_api_hash_here
BOT_TOKEN=your_bot_token_here

# MongoDB Configuration  
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/banbot
DB_NAME=banbot

# Logging Configuration
LOG_GROUP_ID=-1001234567890

# Security Configuration (Comma-separated Telegram user IDs)
SUDO_USERS=123456789,987654321

# Performance Configuration (Optional)
MAX_CONCURRENT_OPERATIONS=10
FLOOD_WAIT_THRESHOLD=30
```

### Step 4: Run the Bot
```bash
python main.py
```

## 🌐 VPS Deployment (Ubuntu 20.04+)

### Quick Deploy Script
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Git
sudo apt install python3 python3-pip git -y

# Clone repository
git clone https://github.com/strad-dev131/BanAll
cd BanAll

# Install dependencies
pip3 install -r requirements.txt

# Configure environment
nano .env
# Add your configuration here

# Test run
python3 main.py
```

### 24/7 Operation with tmux
```bash
# Install tmux
sudo apt install tmux -y

# Create new session
tmux new -s banbot

# Run bot
python3 main.py

# Detach session (Ctrl+B, then D)
# Reattach later: tmux attach -t banbot
```

## 🔧 Configuration Guide

### Telegram API Setup
1. Visit [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy `API_ID` and `API_HASH`

### Bot Token Setup
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Create new bot with `/newbot`
3. Copy the bot token

### MongoDB Setup
1. Create free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Add database user
4. Get connection string
5. Replace in `MONGO_URL`

### Log Group Setup
1. Create a Telegram group for logs
2. Add your bot to the group
3. Make bot admin with message permissions
4. Get group ID (start with -100)

## 📊 Performance Features

### Concurrent Operations
- **Default**: 10 concurrent operations
- **Configurable**: Adjust via `MAX_CONCURRENT_OPERATIONS`
- **Smart Limiting**: Prevents API rate limits

### FloodWait Management
- **Automatic retry** with exponential backoff
- **Configurable threshold** via `FLOOD_WAIT_THRESHOLD`
- **Intelligent waiting** respects Telegram limits

### Memory Optimization
- **Streaming member fetching** for large groups
- **Garbage collection** after operations
- **Minimal memory footprint**

## 🛡️ Security Features

### Access Control
- **Sudo-only commands** - Unauthorized users blocked
- **Admin protection** - Group admins never affected
- **Creator protection** - Group creator always protected
- **Self-protection** - Bot cannot ban itself

### Data Security
- **Environment variables** - No hardcoded secrets
- **Encrypted communications** - TgCrypto for speed
- **Audit logging** - Complete action history

## 📈 Monitoring & Logging

### Database Logging
- **Action logs** with timestamps
- **Group statistics** tracking
- **User activity** monitoring
- **Error tracking** and reporting

### Log Group Updates
- **Real-time notifications** for all actions
- **Detailed statistics** after operations
- **Error alerts** for failed operations

## 🔍 Troubleshooting

### Common Issues

**Bot not responding:**
- Check bot token validity
- Verify bot is added to group
- Ensure bot has admin permissions

**Permission errors:**
- Add bot as admin in group
- Grant necessary permissions (ban users, delete messages)
- Check sudo user configuration

**Database connection failed:**
- Verify MongoDB URL format
- Check network connectivity
- Ensure database user has permissions

**FloodWait errors:**
- Reduce `MAX_CONCURRENT_OPERATIONS`
- Increase `FLOOD_WAIT_THRESHOLD`
- Check API rate limits

### Debug Mode
Enable debug logging by adding to `.env`:
```env
LOG_LEVEL=DEBUG
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Credits

**Developed by:**
- 👤 Telegram: [@Elite_Sid](https://t.me/Elite_Sid)
- 💻 GitHub Team: [strad-dev131](https://github.com/strad-dev131)
- 🛡️ Licensed for use **only by approved sudo users**

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## ⚠️ Disclaimer

This bot is designed for legitimate group management purposes only. Users are responsible for compliance with Telegram's Terms of Service and applicable laws. The developers are not responsible for misuse of this software.

## 📞 Support

For support and updates:
- 📧 Telegram: [@Elite_Sid](https://t.me/Elite_Sid)
- 🐛 Issues: [GitHub Issues](https://github.com/strad-dev131/telegram-banall-bot/issues)
- 📖 Documentation: [Wiki](https://github.com/strad-dev131/BanAll/wiki)

---

**🔥 The most powerful Telegram Ban-All Bot ever created - Built for performance, security, and reliability!**
