#!/usr/bin/env python3
"""
Iqra University AI Chatbot - Pure Python Console Version
A simple, interactive chatbot for university information
"""

import os
import sys
from chatbot import ChatBot

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print welcome banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        🎓  IQRA UNIVERSITY AI CHATBOT  🤖                    ║
║                                                               ║
║        Your Intelligent Assistant for University Info        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)
    print(f"{Colors.GREEN}Welcome! I'm here to help you with information about:")
    print(f"  📚 Academics & Courses")
    print(f"  🎯 Admissions & Requirements")
    print(f"  📋 University Policies")
    print(f"  ℹ️  General Information")
    print(f"\n{Colors.YELLOW}Type 'quit', 'exit', or 'bye' to end the conversation{Colors.END}\n")
    print("─" * 65)

def print_user_message(message):
    """Print user message with formatting"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}You:{Colors.END} {message}")

def print_bot_message(message):
    """Print bot message with formatting"""
    print(f"\n{Colors.GREEN}{Colors.BOLD}AI Assistant:{Colors.END} {message}")

def print_error(message):
    """Print error message"""
    print(f"\n{Colors.RED}❌ Error: {message}{Colors.END}")

def print_thinking():
    """Print thinking indicator"""
    print(f"\n{Colors.CYAN}🤔 Thinking...{Colors.END}", end='', flush=True)

def clear_thinking():
    """Clear thinking indicator"""
    print('\r' + ' ' * 50 + '\r', end='', flush=True)

def get_user_input():
    """Get input from user with prompt"""
    try:
        user_input = input(f"\n{Colors.BOLD}💬 Your message: {Colors.END}").strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        return 'quit'

def main():
    """Main chatbot loop"""
    # Clear screen and show banner
    clear_screen()
    print_banner()
    
    # Initialize chatbot
    try:
        print(f"{Colors.CYAN}Initializing AI Assistant...{Colors.END}")
        bot = ChatBot()
        print(f"{Colors.GREEN}✓ AI Assistant ready!{Colors.END}\n")
    except Exception as e:
        print_error(f"Failed to initialize chatbot: {str(e)}")
        print(f"\n{Colors.YELLOW}Please check your API key and internet connection.{Colors.END}")
        return
    
    # Conversation counter
    conversation_count = 0
    
    # Main conversation loop
    while True:
        # Get user input
        user_message = get_user_input()
        
        # Check for empty input
        if not user_message:
            print(f"{Colors.YELLOW}Please enter a message.{Colors.END}")
            continue
        
        # Check for exit commands
        if user_message.lower() in ['quit', 'exit', 'bye', 'goodbye', 'q']:
            print(f"\n{Colors.CYAN}{Colors.BOLD}Thank you for using Iqra University AI Chatbot!{Colors.END}")
            print(f"{Colors.GREEN}Have a great day! 👋{Colors.END}\n")
            break
        
        # Display user message
        print_user_message(user_message)
        
        # Show thinking indicator
        print_thinking()
        
        # Get bot response
        try:
            response = bot.get_response(user_message)
            clear_thinking()
            print_bot_message(response)
            conversation_count += 1
            
        except Exception as e:
            clear_thinking()
            print_error(f"Failed to get response: {str(e)}")
            print(f"{Colors.YELLOW}Please try again or check your connection.{Colors.END}")
        
        # Add separator after each exchange
        print(f"\n{Colors.CYAN}{'─' * 65}{Colors.END}")
    
    # Show conversation statistics
    if conversation_count > 0:
        print(f"\n{Colors.CYAN}📊 Conversation Summary:{Colors.END}")
        print(f"   Total messages exchanged: {conversation_count}")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Chatbot interrupted by user.{Colors.END}")
        print(f"{Colors.GREEN}Goodbye! 👋{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)
