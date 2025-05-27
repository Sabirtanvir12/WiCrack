# WiCrack 🔓📡

![WiCrack Banner](https://i.postimg.cc/nzW6GN6D/Screenshot-2025-05-27-111520.png)  
*A next-generation WiFi security auditing tool with brute-force capabilities*

**Version:** 3.0  
**Developer:** Sabir Tanvir  
**GitHub:** [github.com/Sabirtanvir12/WiCrack](https://github.com/Sabirtanvir12/WiCrack)  
**License:** MIT  

## Key Features ✨

| Feature | Description |
|---------|-------------|
| **Cross-Platform** | Windows & Linux support with automatic OS detection |
| **Smart Interface** | Auto-detects available WiFi interfaces |
| **Advanced Scanning** | Detailed network scanning with signal strength metrics |
| **Wordlist Engine** | Supports custom wordlists >10GB with optimized loading |
| **Live Progress** | Real-time attack statistics with ETA calculation |
| **Auto-Elevation** | Automatically requests admin/root privileges |
| **Result Logging** | Saves successful cracks with timestamps |

    Architecture:

    A --> [Network Scanner]
    B --> C[Target Selection]
    C --> D[Wordlist Processor]
    D --> E[Brute Force Engine]
    E --> F[Result Logger]

## Installation ⚡

### Prerequisites
- Python 3.8+
- `comtypes` (Windows only)
- Wireless interface in monitor mode (Linux)
---
## Installation  
**Linux:**

   ```bash
  git clone https://github.com/Sabirtanvir12/WiCrack.git
  cd WiCrack
  ```

  ```bash
  pip install pywifi comtypes
  ```

  ```bash
  python3 wicrack.py
  ```
---
---
### 💻 Windows
1. Download the ZIP file from GitHub and extract it.
2. Open the extracted folder.
3. Right-click inside the folder and select **Open in Terminal**.
4. Install dependencies:
   ```powershell
   pip install pywifi comtypes
   ```

5. Run the script using:
   ```powershell
   Duble click then run with ide or python debuger
   ```

---
   ## 📜 License

🔒 This project is licensed under the **MIT License**. See the `LICENSE` file for more details.  

---
## ❤️ Support

If you like this project, don't forget to **⭐ star the repo**! 😊  

📧 For any queries, reach out via **[sabirtanvir10@gmail.com](mailto:sabirtanvir10@gmail.com)** or open an **issue**. 
