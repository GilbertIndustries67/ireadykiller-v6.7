import time
from win10toast import ToastNotifier
toaster = ToastNotifier()

while True:
    try:
        import mss
        import mss.tools
        from google import genai
        from google.genai import types
        from yaspin import yaspin
        from win10toast import ToastNotifier
        import keyboard

        API_KEY = ""
#ur api key here for gemini
        client = genai.Client(api_key=API_KEY)
        toaster = ToastNotifier()

        CAP_W = 1226
        CAP_H = 918
        #pip install mss google-genai yaspin win10toast keyboard requests

        # ------------------------
        # WRAP LOGIC INTO FUNCTION
        # ------------------------
        def capture_and_solve():
            # Screenshot
            with mss.mss() as sct:
                toaster.show_toast("Thinking...", " ", duration=1)
                mon = sct.monitors[1]  # Primary monitor

                screen_width = mon["width"]
                screen_height = mon["height"]

                left = (screen_width - CAP_W) // 2
                top = (screen_height - CAP_H) // 2

                monitor = {
                    "top": top,
                    "left": left,
                    "width": CAP_W,
                    "height": CAP_H
                }

                sct_img = sct.grab(monitor)

                output_path = "screenshot_centered.png"
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)

                print(f"Screenshot saved as {output_path}")

            # AI Processing
            with yaspin(text="Thinking...", color="cyan") as spinner:
                
                with open("screenshot_centered.png", "rb") as f:
                    image_bytes = f.read()

                image_part = types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/png'
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        image_part,
                        'Solve this problem in the screenshot with no explanation. Just give the final answer. with no markdown styling, just plain text.'
                    ]
                )

                spinner.ok("✔")

            # Show result
            print("Gemini Response:")
            print(response.text)
            print("\n-----------------------------------------\n")
            toaster.show_toast("Answer", response.text, duration=5)

        # ------------------------
        # HOTKEY LISTENER
        # ------------------------
        toaster.show_toast("Started", "Press F8 to trigger, and ctrl-c in terminal to close.", duration=5)
        keyboard.add_hotkey("F8", capture_and_solve)

        keyboard.wait()

    except Exception as e:
        toaster.show_toast("Crashed","Restarting...", duration=5)
        time.sleep(2)
