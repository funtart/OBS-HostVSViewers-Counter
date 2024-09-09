import obspython as S
import winsound
import time
import threading

__version__ = "1.1.0"

class TextContent:
    def __init__(self, source_name=None, text_string="This is default text"):
        self.source_name = source_name
        self.text_string = text_string
        self.counter = 0

    def update_text(self, counter_text, counter_value=0):
        source = S.obs_get_source_by_name(self.source_name)
        settings = S.obs_data_create()
        if counter_value == 1:
            self.counter += 1
        if counter_value == -1:
            self.counter -= 1
        if counter_value == 0:
            self.counter = 0
        if isinstance(counter_value, str):
            self.counter = int(counter_value)

        self.text_string = f"{counter_text}{self.counter}"

        S.obs_data_set_string(settings, "text", self.text_string)
        S.obs_source_update(source, settings)
        S.obs_data_release(settings)
        S.obs_source_release(source)


class Driver(TextContent):
    def increment(self):
        self.update_text(self.counter_text, 1)
        self.play_sound(self.sound_file)

    def play_sound(self, sound_file):
        if sound_file:
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)

    def decrement(self):
        self.update_text(self.counter_text, -1)

    def reset(self):
        self.update_text(self.counter_text, 0)

    def do_custom(self, val):
        self.update_text(self.counter_text, str(val))


class Hotkey:
    def __init__(self, callback, obs_settings, _id):
        self.obs_data = obs_settings
        self.hotkey_id = S.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = _id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        description = "Htk " + str(self._id)
        self.hotkey_id = S.obs_hotkey_register_frontend(
            "htk_id" + str(self._id), description, self.callback
        )
        S.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        self.hotkey_saved_key = S.obs_data_get_array(
            self.obs_data, "htk_id" + str(self._id)
        )
        S.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        self.hotkey_saved_key = S.obs_hotkey_save(self.hotkey_id)
        S.obs_data_set_array(
            self.obs_data, "htk_id" + str(self._id), self.hotkey_saved_key
        )
        S.obs_data_array_release(self.hotkey_saved_key)


class HotkeyDataHolder:
    htk_copy = None  # this attribute will hold an instance of Hotkey


hotkeys_counter_1 = Driver()
hotkeys_counter_2 = Driver()

h01 = HotkeyDataHolder()
h02 = HotkeyDataHolder()
h03 = HotkeyDataHolder()
h11 = HotkeyDataHolder()
h12 = HotkeyDataHolder()
h13 = HotkeyDataHolder()
h21 = HotkeyDataHolder()
h22 = HotkeyDataHolder()
h23 = HotkeyDataHolder()


class Timer(Driver):
    def __init__(self, source_name=None, start_time=60):
        super().__init__(source_name)
        self.start_time = start_time  # In seconds
        self.remaining_time = start_time
        self.timer_running = False
        self.timer_thread = None
        self.sound_file = ""  # Default value

    def start_timer(self):
        if not self.timer_running:
            print(f"Starting timer with {self.remaining_time} seconds left.")  # Debug print
            self.timer_running = True
            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

    def run_timer(self):
        while self.timer_running and self.remaining_time > 0:
            time.sleep(1)  # 1 second interval
            self.remaining_time -= 1
            self.update_display()

        if self.remaining_time <= 0:
            self.timer_running = False
            self.remaining_time = 0
            print(f"Timer ended. Playing sound.")  # Debug print
            self.play_sound(self.sound_file)  # Play sound when timer ends

    def update_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.text_string = f"{minutes:02}:{seconds:02}"
        print(f"Updating display to: {self.text_string}")  # Debug print
        source = S.obs_get_source_by_name(self.source_name)
        if source:
            settings = S.obs_data_create()
            S.obs_data_set_string(settings, "text", self.text_string)
            S.obs_source_update(source, settings)
            S.obs_data_release(settings)
            S.obs_source_release(source)
        else:
            print(f"Source {self.source_name} not found.")  # Debug print

    def reset_timer(self):
        self.timer_running = False
        self.remaining_time = self.start_time
        print(f"Resetting timer. Start time: {self.start_time}, Remaining time: {self.remaining_time}")  # Debug print
        self.update_display()

    def stop_timer(self):
        self.timer_running = False

    def play_sound(self, sound_file):
        # Add implementation to play sound file
        print(f"Playing sound: {sound_file}")  # Debug print


# Initialize timers
countdown_timer = Timer()


# Hotkey callbacks for the timer
def callback_start_timer(pressed):
    if pressed:
        countdown_timer.start_timer()


def callback_reset_timer(pressed):
    if pressed:
        countdown_timer.reset_timer()


# Counter 1 hotkey callbacks
def callback_up1(pressed):
    if pressed:
        return hotkeys_counter_1.increment()


def callback_down1(pressed):
    if pressed:
        return hotkeys_counter_1.decrement()


def callback_reset1(pressed):
    if pressed:
        return hotkeys_counter_1.reset()


def callback_custom1(*args):
    hotkeys_counter_1.do_custom(S.obs_data_get_int(args[2], "counter_1"))
    return True


# Counter 2 hotkey callbacks
def callback_up2(pressed):
    if pressed:
        return hotkeys_counter_2.increment()


def callback_down2(pressed):
    if pressed:
        return hotkeys_counter_2.decrement()


def callback_reset2(pressed):
    if pressed:
        return hotkeys_counter_2.reset()


def callback_custom2(*args):
    hotkeys_counter_2.do_custom(S.obs_data_get_int(args[2], "counter_2"))
    return True

# Define callback functions for timer control
def callback_start_timer(pressed):
    if pressed:
        timer.start_timer()

def callback_reset_timer(pressed):
    if pressed:
        timer.reset_timer()

def callback_custom3(*args):
    countdown_timer.start_time = S.obs_data_get_int(args[2], "start_timer")
    # countdown_timer.reset_timer()  # Reset timer to reflect new start time
    return True




# OBS script description
def script_description():
    return "Multiple Counters with Timer"


# OBS script update function
def script_update(settings):
    hotkeys_counter_1.source_name = S.obs_data_get_string(settings, "source1")
    hotkeys_counter_1.counter_text = S.obs_data_get_string(settings, "counter_text1")
    hotkeys_counter_1.sound_file = S.obs_data_get_string(settings, "sound_file1")

    hotkeys_counter_2.source_name = S.obs_data_get_string(settings, "source2")
    hotkeys_counter_2.counter_text = S.obs_data_get_string(settings, "counter_text2")
    hotkeys_counter_2.sound_file = S.obs_data_get_string(settings, "sound_file2")

    countdown_timer.source_name = S.obs_data_get_string(settings, "timer_source")
    countdown_timer.start_time = S.obs_data_get_int(settings, "start_time")
    countdown_timer.sound_file = S.obs_data_get_string(settings, "timer_sound_file")
    countdown_timer.reset_timer() 


# OBS script properties
def script_properties():
    props = S.obs_properties_create()

    # Counter 1 properties
    S.obs_properties_add_text(
        props, "counter_text1", "[1]Set counter text", S.OBS_TEXT_DEFAULT
    )
    p = S.obs_properties_add_int(
        props, "counter_1", "Set custom value", -999999, 999999, 1
    )
    S.obs_property_set_modified_callback(p, callback_custom1)
    p1 = S.obs_properties_add_list(
        props,
        "source1",
        "[1]Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    # Add file selector for counter 1 sound
    S.obs_properties_add_path(
        props, "sound_file1", "[1]Sound for increment", S.OBS_PATH_FILE, "Audio files (*.wav *.mp3)", None
    )

    # Counter 2 properties
    S.obs_properties_add_text(
        props, "counter_text2", "[2]Set counter text", S.OBS_TEXT_DEFAULT
    )
    p = S.obs_properties_add_int(
        props, "counter_2", "Set custom value", -999999, 999999, 1
    )
    S.obs_property_set_modified_callback(p, callback_custom2)
    p2 = S.obs_properties_add_list(
        props,
        "source2",
        "[2]Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    # Add file selector for counter 2 sound
    S.obs_properties_add_path(
        props, "sound_file2", "[2]Sound for increment", S.OBS_PATH_FILE, "Audio files (*.wav *.mp3)", None
    )

    # Timer properties
    p = S.obs_properties_add_int(
        props, "start_time", "Timer Start Time (seconds)", 1, 3600, 1
    )
    S.obs_property_set_modified_callback(p, callback_custom3)
    p_timer = S.obs_properties_add_list(
        props,
        "timer_source",
        "Timer Text Source",
        S.OBS_COMBO_TYPE_EDITABLE,
        S.OBS_COMBO_FORMAT_STRING,
    )

    # Add file selector for timer sound
    S.obs_properties_add_path(
        props, "timer_sound_file", "Sound for Timer End", S.OBS_PATH_FILE, "Audio files (*.wav *.mp3)", None
    )

    # Enum all available text sources
    sources = S.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = S.obs_source_get_unversioned_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = S.obs_source_get_name(source)
                # Add sources to counter 1, counter 2, and timer dropdowns
                S.obs_property_list_add_string(p1, name, name)
                S.obs_property_list_add_string(p2, name, name)
                S.obs_property_list_add_string(p_timer, name, name)

            S.obs_source_release(source)  # Release the source after usage

    return props


# OBS script load/save functions
def script_load(settings):
    global timer
    # Load counter settings
    hotkeys_counter_1.counter = S.obs_data_get_int(settings, "counter1")
    hotkeys_counter_2.counter = S.obs_data_get_int(settings, "counter2")

    # Load hotkeys
    h01.htk_copy = Hotkey(callback_up1, settings, "count_up1")
    h02.htk_copy = Hotkey(callback_down1, settings, "count_down1")
    h03.htk_copy = Hotkey(callback_reset1, settings, "reset1")

    h11.htk_copy = Hotkey(callback_up2, settings, "count_up2")
    h12.htk_copy = Hotkey(callback_down2, settings, "count_down2")
    h13.htk_copy = Hotkey(callback_reset2, settings, "reset2")

    # Load timer settings
    timer_start_time = S.obs_data_get_int(settings, "start_time")  # Ensure this is set correctly
    timer_source_name = S.obs_data_get_string(settings, "timer_source")
    timer_sound_file = S.obs_data_get_string(settings, "timer_sound_file")

    print(f"Loaded timer_start_time: {timer_start_time}")

    timer = Timer(source_name=timer_source_name, start_time=timer_start_time)
    timer.sound_file = timer_sound_file

    # Load and set up hotkeys for timer control
    h21.htk_copy = Hotkey(callback_start_timer, settings, "start_timer")
    h22.htk_copy = Hotkey(callback_reset_timer, settings, "reset_timer")



def script_save(settings):
    # Save counter settings
    S.obs_data_set_int(settings, "counter1", hotkeys_counter_1.counter)
    S.obs_data_set_int(settings, "counter2", hotkeys_counter_2.counter)

    # Save sound file paths
    S.obs_data_set_string(settings, "sound_file1", hotkeys_counter_1.sound_file)
    S.obs_data_set_string(settings, "sound_file2", hotkeys_counter_2.sound_file)

    # Save timer settings
    S.obs_data_set_int(settings, "timer_start_time", timer.start_time)
    S.obs_data_set_string(settings, "timer_source", timer.source_name)
    S.obs_data_set_string(settings, "timer_sound_file", timer.sound_file)

    # Save hotkeys
    for h in [h01, h02, h03, h11, h12, h13, h21, h22]:
        h.htk_copy.save_hotkey()




description = """
<h2>Version : {__version__}</h2>
<a href="https://github.com/upgradeQ/Obscounter"> Webpage </a>
<h3 style="color:orange">Authors</h3>
<a href="https://github.com/upgradeQ"> upgradeQ </a> <br>
""".format(
    **locals()
)


def script_description():
    print(description, "Released under MIT license")
    return description
