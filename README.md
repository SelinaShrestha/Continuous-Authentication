# Continuous Authentication Using Secret Sharing

## 📌 Overview
This project implements a **continuous authentication protocol** using **secret sharing** for **IoT mesh networks**. The authentication mechanism ensures that users remain continuously authenticated in a secure environment without requiring frequent re-authentication.

This work is based on our research paper:
> **S. Shrestha, M. A. Lopez, M. Baddeley, S. Muhaidat and J. -P. Giacalone,**  
> "*A Time-Bound Continuous Authentication Protocol for Mesh Networking,*"  
> 2021 4th International Conference on Advanced Communication Technologies and Networking (CommNet), Rabat, Morocco, 2021, pp. 1-6, doi: [10.1109/CommNet52204.2021.9641895](https://doi.org/10.1109/CommNet52204.2021.9641895).

## 🚀 Features
- Secure authentication using **secret sharing**
- Client-server architecture for authentication management
- Implements **Cyclic Redundancy Check (CRC)** for integrity verification
- Ensures seamless and **continuous authentication** in real-time
- **Lightweight protocol** for constrained IoT mesh networks

## 🛠️ Technologies Used
- **Programming Language:** Python
- **Networking:** Sockets for client-server communication
- **Security:** Secret Sharing, Hashing, CRC for data validation

## 🏗️ Project Structure
```
/Continuous-Authentication
├── src/
│   ├── client.py              # Client-side authentication
│   ├── client_functions.py    # Client-side helper functions
│   ├── server.py              # Server-side authentication management
│   ├── server_functions.py    # Server-side helper functions
│   └── crc_functions.py       # CRC functions for error checking
├── docs/
│   ├── continuous_authentication_algorithm.md  # Technical documentation
│   └── algorithm_diagram.png  # Technical diagram for documentation
├── README.md                  # Project Overview
├── requirements.txt           # Required Python packages
└── .gitignore                 # Ignoring unnecessary files
```

## 🔧 Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/SelinaShrestha/Continuous-Authentication.git
   cd Continuous-Authentication
   ```

2. **Install Dependencies** (if required)
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Server**
   ```bash
   python src/server.py
   ```

4. **Run the Client**
   ```bash
   python src/client.py
   ```

## 📝 Usage
- The **server** listens for authentication requests.
- The **client** continuously authenticates itself by interacting with the server.
- Secret-sharing techniques ensure the authentication remains secure.

## 📄 Documentation
For a detailed explanation of the **Secret Sharing Based Continuous Authentication Algorithm**, refer to:
- [`docs/continuous_authentication_algorithm.md`](docs/continuous_authentication_algorithm.md)

For performance evaluation, refer to:
- [**Published Paper (IEEE Xplore)**](https://doi.org/10.1109/CommNet52204.2021.9641895)


## 📬 Contact
For any inquiries, feel free to reach out:
- **GitHub:** [SelinaShrestha](https://github.com/SelinaShrestha)
- **LinkedIn:** [selinashrestha](https://www.linkedin.com/in/selinashrestha/)
- **Email:** shresth4@uci.edu | selina.shrestha0@gmail.com

