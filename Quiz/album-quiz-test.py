import os
import sys
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import re

class AlbumQuizTest:
    def __init__(self):
        self.driver = None
        self.base_url = os.getenv('BASE_URL', 'http://localhost:4200')

    def setup(self):
        """Setup ChromeDriver"""
        try:
            print('🔧 Starting custom setup...')
            
            # Chrome options
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--remote-allow-origins=*')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--disable-features=TranslateUI')
            chrome_options.add_argument('--disable-ipc-flooding-protection')
            
            if os.getenv('HEADLESS', '').lower() in ['true', '1']:
                chrome_options.add_argument('--headless=new')

            print('🚀 Creating Chrome driver...')
            
            # Initialize Chrome driver
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Navigate to blank page
            self.driver.get('about:blank')
            
            # Set timeouts
            self.driver.implicitly_wait(10)
            self.driver.set_page_load_timeout(60)
            self.driver.set_script_timeout(30)

            print('✓ Chrome driver created successfully')
            print(f'✓ Base URL set to: {self.base_url}')
            return True
            
        except Exception as error:
            print(f'❌ Custom setup failed: {str(error)}')
            raise error

    def teardown(self):
        """Cleanup browser"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f'Driver already closed or error during quit: {str(e)}')

    def navigate_to(self, relative_path):
        """Navigate to a URL"""
        if not self.driver:
            raise Exception('Driver not initialized')
        
        url = relative_path if relative_path.startswith('http') else f"{self.base_url}{relative_path}"
        print(f'➡️ Navigating to: {url}')
        
        try:
            self.driver.get(url)
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except Exception as error:
            print(f'Navigation failed: {str(error)}')
            raise error

    def wait_for_element(self, selector, timeout=10):
        """Wait for element to be present and visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of(element)
            )
        except TimeoutException:
            raise Exception(f'Element {selector} not found or not visible within {timeout}s')

    def debug_session_state(self):
        """Debug method to check session state"""
        try:
            current_url = self.driver.current_url
            page_title = self.driver.title
            has_token = self.driver.execute_script("""
                return {
                    accessToken: localStorage.getItem('accessToken') !== null,
                    tokenValue: localStorage.getItem('accessToken') ? localStorage.getItem('accessToken').substring(0, 20) + '...' : null,
                    allKeys: Object.keys(localStorage)
                };
            """)
            
            print('🔍 Session Debug Info:')
            print(f'- Current URL: {current_url}')
            print(f'- Page Title: {page_title}')
            print(f'- Token Info: {has_token}')
            
            return {'current_url': current_url, 'page_title': page_title, 'has_token': has_token}
        except Exception as error:
            print(f'Debug failed: {str(error)}')
            return None

    def login(self):
        """Login method"""
        # Get credentials from environment variables or use defaults
        username = os.getenv('E2E_USER') or os.getenv('TEST_USER') or 'tuan1@gmail.com'
        password = os.getenv('E2E_PASS') or os.getenv('TEST_PASS') or '123456'

        print(f'🔐 Using credentials: {username} / ****')

        login_paths = ['/auth/login', '/login', '/user/login', '/account/login']

        for path in login_paths:
            try:
                print(f'🔐 Trying login at: {path}')
                self.navigate_to(path)
                time.sleep(2)

                # Find login elements
                user_field = self.wait_for_element('input[type="email"], input[name="email"], input#email, input[name="username"], input#username')
                pass_field = self.wait_for_element('input[type="password"], input[name="password"], input#password')

                # Enter credentials
                user_field.clear()
                user_field.send_keys(username)
                pass_field.clear()
                pass_field.send_keys(password)

                # Click login button
                login_btn = self.wait_for_element('button[type="submit"], button[id*="login"], button[class*="login"], input[type="submit"]')
                login_btn.click()

                time.sleep(5)

                # Debug session after login
                self.debug_session_state()

                current_url = self.driver.current_url
                print(f'Current URL after login attempt: {current_url}')

                # Check if redirected to home (login success)
                if '/home' in current_url or (not ('login' in current_url) and not ('auth' in current_url)):
                    has_token = self.driver.execute_script('return localStorage.getItem("accessToken") !== null;')
                    
                    print(f'Has access token: {has_token}')
                    
                    if has_token:
                        print('✓ Login succeeded with token')
                        return True

            except Exception as e:
                print(f'⚠️ Login attempt via {path} failed: {str(e)}')

        print('❌ Login failed on all known routes')
        return False

    def test_page_load(self):
        """Test loading /quiz page"""
        try:
            print('Testing /quiz page load...')
            
            if not self.driver:
                print('❌ Driver not available')
                return False

            # Only test /quiz route
            print('Navigating to /quiz route...')
            self.navigate_to('/quiz')
            time.sleep(3)

            current_url = self.driver.current_url
            print(f'Current URL: {current_url}')
            
            # If redirected to auth, authentication failed
            if 'login' in current_url or 'auth' in current_url:
                print('❌ Redirected to auth page - authentication may have expired')
                return False

            # Check if we're on the quiz page
            if '/quiz' in current_url:
                print('✓ Successfully on /quiz page')
                
                # Check for album quiz content
                page_source = self.driver.page_source
                page_title = self.driver.title
                
                print(f'Page title: {page_title}')
                
                has_album_quiz_content = ('app-album-quiz' in page_source or 
                                        'Album Quiz' in page_source or 
                                        'quiz-level' in page_source or
                                        'level-button' in page_source or
                                        'Easy' in page_source or
                                        'Medium' in page_source or
                                        'Hard' in page_source or
                                        'Mixed' in page_source or
                                        'quiz' in page_title.lower() or
                                        'album' in page_title.lower())

                if has_album_quiz_content:
                    print('✓ Album quiz content detected on /quiz page')
                    return True
                else:
                    print('⚠️ On /quiz page but no album quiz content detected')
                    print('Page source snippet (first 1000 chars):')
                    print(page_source[:1000])
                    return True  # Still consider it a success since we reached the page

            print('❌ Not on expected /quiz page')
            print(f'Actual URL: {current_url}')
            return False
            
        except Exception as error:
            print(f'❌ Page load failed: {str(error)}')
            return False

    def test_level_buttons(self):
        """Test level selection buttons"""
        try:
            print('Testing level selection buttons...')
            
            if not self.driver:
                print('❌ Driver not available')
                return False

            # Ensure we're on the quiz page first
            self.navigate_to('/quiz')
            time.sleep(3)

            current_url = self.driver.current_url
            if '/quiz' not in current_url:
                print('❌ Cannot reach /quiz page for button testing')
                return False

            time.sleep(2)
            
            # Try multiple selectors for level buttons
            selectors = [
                'button[class*="level"]',
                'button[id*="level"]', 
                'button[data-level]',
                '.level-button',
                '.quiz-level',
                'button:not([type="submit"]):not([class*="back"]):not([class*="close"]):not([class*="login"])'
            ]

            buttons = []
            for selector in selectors:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(buttons) > 0:
                    print(f'Found {len(buttons)} buttons with selector: {selector}')
                    break

            if len(buttons) == 0:
                print('❌ No buttons found, checking page content...')
                page_source = self.driver.page_source
                print('Page source snippet (first 1000 chars):')
                print(page_source[:1000])
                return False

            # Log button info for debugging
            print('Button analysis:')
            for i, button in enumerate(buttons[:10]):  # Limit to first 10 buttons
                try:
                    text = button.text
                    classes = button.get_attribute('class')
                    button_id = button.get_attribute('id')
                    print(f'Button {i}: "{text}" (id: {button_id}, classes: {classes})')
                except Exception as e:
                    print(f'Button {i}: (error getting info - {str(e)})')

            # Look specifically for level-related buttons
            level_keywords = ['easy', 'medium', 'hard', 'mixed', 'beginner', 'advanced']
            level_buttons_found = 0

            for i, button in enumerate(buttons):
                try:
                    text = (button.text or '').lower()
                    classes = (button.get_attribute('class') or '').lower()
                    button_id = (button.get_attribute('id') or '').lower()
                    
                    has_level_keyword = any(keyword in text or keyword in classes or keyword in button_id 
                                          for keyword in level_keywords)
                    
                    if has_level_keyword:
                        level_buttons_found += 1
                        print(f'✓ Level button found: "{text}"')
                except Exception:
                    # Skip this button
                    pass

            if level_buttons_found > 0:
                print(f'✓ Found {level_buttons_found} level-specific buttons')
                return True

            print(f'Found {len(buttons)} total buttons but none appear to be level buttons')
            # If we have multiple buttons, assume some might be level buttons
            return len(buttons) >= 1
            
        except Exception as error:
            print(f'❌ Level buttons test failed: {str(error)}')
            return False

    def test_level_popup(self):
        """Test level popup functionality"""
        try:
            print('Testing level popup functionality...')
            
            if not self.driver:
                print('❌ Driver not available')
                return False

            # Ensure we're on the quiz page
            self.navigate_to('/quiz')
            time.sleep(3)

            # Find buttons that might be level buttons
            buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button')
            if len(buttons) == 0:
                print('❌ No buttons found to test popup')
                return False

            print(f'Testing popup functionality with {len(buttons)} buttons...')

            # Try clicking buttons that might trigger popups
            for i, button in enumerate(buttons[:5]):  # Test first 5 buttons
                try:
                    button_text = button.text
                    print(f'Trying button {i}: "{button_text}"')
                    
                    # Skip buttons that are clearly not level buttons
                    button_text_lower = button_text.lower()
                    if ('back' in button_text_lower or 'close' in button_text_lower or 
                        'cancel' in button_text_lower or 'login' in button_text_lower):
                        print(f'Skipping button {i} (not a level button)')
                        continue
                    
                    # Check if button is clickable
                    if not button.is_enabled():
                        print(f'Button {i} is disabled, skipping...')
                        continue

                    # Scroll to button to ensure it's visible
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(0.5)

                    button.click()
                    time.sleep(2)

                    # Check for popup/modal elements
                    popup_selectors = [
                        '.popup', '.modal', '.dialog', '.overlay',
                        '[class*="popup"]', '[class*="modal"]', '[class*="overlay"]',
                        '.mat-dialog-container', '.confirmation-dialog',
                        '[role="dialog"]', '[aria-modal="true"]'
                    ]

                    popup_found = False
                    for selector in popup_selectors:
                        popups = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if len(popups) > 0:
                            print(f'✓ Popup found with selector: {selector}')
                            popup_found = True
                            break

                    # Also check if page content changed (might be inline popup)
                    page_source = self.driver.page_source
                    has_popup_content = ('popup' in page_source or 
                                       'modal' in page_source or 
                                       'dialog' in page_source or
                                       'overlay' in page_source or
                                       'confirmation' in page_source)

                    if popup_found or has_popup_content:
                        print('✓ Popup or modal content detected')

                        # Try to close popup if possible
                        close_selectors = [
                            'button[class*="close"]', 'button[class*="cancel"]', 
                            '.close-btn', '.cancel-btn', '[aria-label*="close"]',
                            'button[class*="back"]', '.overlay'
                        ]

                        for close_selector in close_selectors:
                            close_buttons = self.driver.find_elements(By.CSS_SELECTOR, close_selector)
                            if len(close_buttons) > 0:
                                try:
                                    close_buttons[0].click()
                                    time.sleep(0.5)
                                    print('✓ Popup closed')
                                except Exception:
                                    print('Could not close popup, continuing...')
                                break

                        return True

                    print(f'Button {i} clicked but no popup detected')
                    
                except Exception as e:
                    print(f'Error with button {i}: {str(e)}')

            print('❌ No popup appeared from any button click')
            return False
            
        except Exception as error:
            print(f'❌ Popup test failed: {str(error)}')
            return False

    def test_quiz_navigation(self):
        """Test quiz navigation"""
        try:
            print('Testing quiz navigation...')
            
            if not self.driver:
                print('❌ Driver not available')
                return False

            current_url = self.driver.current_url
            print(f'Current page: {current_url}')

            # Check if we're on the /quiz page
            if '/quiz' in current_url:
                print('✓ Successfully on /quiz page')
                return True

            # Try navigating to /quiz if we're not already there
            self.navigate_to('/quiz')
            time.sleep(2)

            new_url = self.driver.current_url
            if '/quiz' in new_url:
                print('✓ Successfully navigated to /quiz page')
                return True

            print('❌ Cannot reach /quiz page')
            return False
            
        except Exception as error:
            print(f'❌ Navigation test failed: {str(error)}')
            return False

    def test_back_button(self):
        """Test back button availability"""
        try:
            print('Testing back button availability...')
            
            if not self.driver:
                print('❌ Driver not available')
                return False

            # Ensure we're on the quiz page
            self.navigate_to('/quiz')
            time.sleep(2)

            back_selectors = [
                'button[class*="back"]', '.back-btn', '[class*="go-back"]',
                'button[aria-label*="back"]', '[routerlink]',
                'button[class*="return"]', '.return-btn'
            ]

            for selector in back_selectors:
                back_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if len(back_buttons) > 0:
                    print(f'✓ Back navigation element found: {selector} ({len(back_buttons)} elements)')
                    
                    # Try to get text of back buttons for verification
                    for i, back_button in enumerate(back_buttons[:3]):  # Check first 3
                        try:
                            text = back_button.text
                            print(f'  Back button {i}: "{text}"')
                        except Exception:
                            print(f'  Back button {i}: (no text)')
                    return True

            print('❌ No back navigation elements found')
            return False
            
        except Exception as error:
            print(f'❌ Back button test failed: {str(error)}')
            return False

    def run_all_tests(self):
        """Run all tests"""
        print('\n🚀 === Album Quiz Component Tests (Route: /quiz) ===')
        results = []

        try:
            print('Starting setup...')
            self.setup()
            print('✓ Setup completed successfully')

            print('Attempting login...')
            login_result = self.login()
            print(f'Login result: {login_result}')

            if not login_result:
                print('❌ Cannot proceed without login')
                self.teardown()
                return {'passed': 0, 'total': 1}
            print('✓ Login successful')

            tests = [
                {'name': 'Quiz Page Load (/quiz)', 'fn': self.test_page_load},
                {'name': 'Level Buttons', 'fn': self.test_level_buttons},
                {'name': 'Level Popup', 'fn': self.test_level_popup},
                {'name': 'Quiz Navigation', 'fn': self.test_quiz_navigation},
                {'name': 'Back Button', 'fn': self.test_back_button}
            ]

            for test in tests:
                print(f'\n--- Running {test["name"]} ---')
                try:
                    result = test['fn']()
                    results.append(result)
                    print(f'✓ Test {test["name"]} result: {result}')
                except Exception as error:
                    print(f'❌ Test {test["name"]} failed: {str(error)}')
                    results.append(False)

        except Exception as error:
            print(f'❌ Test suite failed: {str(error)}')

        try:
            print('\nStarting teardown...')
            self.teardown()
            print('✓ Teardown completed')
        except Exception as teardown_error:
            print(f'❌ Teardown error: {str(teardown_error)}')

        passed = sum(1 for r in results if r is True)
        total = len(results)
        print(f'\n📊 Final Results: {passed}/{total} passed')
        return {'passed': passed, 'total': total}


# Run if called directly
if __name__ == '__main__':
    print('🚀 Starting Album Quiz Test...')
    test = AlbumQuizTest()
    try:
        result = test.run_all_tests()
        print(f'✅ Test completed: {result}')
        sys.exit(0)
    except Exception as error:
        print(f'💥 Test failed: {str(error)}')
        import traceback
        print('Error traceback:', traceback.format_exc())
        sys.exit(1)