import sys
from configparser import ConfigParser
import tkinter as tk
from typing import Callable, Any, Tuple, List, Dict
import os
import json

import cv2
import numpy as np
from PIL import ImageTk, Image, ImageGrab

COLOR_BG = 'grey19'
COLOR_FG_WHITE = 'snow'
COLOR_FG_GREEN = 'green3'
COLOR_FG_ORANGE = 'orange2'
FONT_BIG = ('Consolas', '14')
FONT_SMALL = ('Consolas', '9')

class ArchnemesisItemsMap:
    """
    Holds the information about all archnemesis items, recipes, images and map them together
    """
    def __init__(self, scale: float):
        # Put everything into the list so we could maintain the display order
        self._arch_items = [
            ('Kitava-Touched', ['Tukohama-Touched', 'Abberath-Touched', 'Corrupter', 'Corpse Detonator']),
            ('Innocence-Touched', ['Lunaris-Touched', 'Solaris-Touched', 'Mirror Image', 'Mana Siphoner']),
            ('Shakari-Touched', ['Entangler', 'Soul Eater', 'Drought Bringer']),
            ('Abberath-Touched', ['Flame Strider', 'Frenzied', 'Rejuvenating']),
            ('Tukohama-Touched', ['Bonebreaker', 'Executioner', 'Magma Barrier']),
            ('Brine King-Touched', ['Ice Prison', 'Storm Strider', 'Heralding Minions']),
            ('Arakaali-Touched', ['Corpse Detonator', 'Entangler', 'Assassin']),
            ('Solaris-Touched', ['Invulnerable', 'Magma Barrier', 'Empowered Minions']),
            ('Lunaris-Touched', ['Invulnerable', 'Frost Strider', 'Empowered Minions']),
            ('Effigy', ['Hexer', 'Malediction', 'Corrupter']),
            ('Empowered Elements', ['Evocationist', 'Steel-Infused', 'Chaosweaver']),
            ('Crystal-Skinned', ['Permafrost', 'Rejuvenating', 'Berserker']),
            ('Invulnerable', ['Sentinel', 'Juggernaut', 'Consecrator']),
            ('Corrupter', ['Bloodletter', 'Chaosweaver']),
            ('Mana Siphoner', ['Consecrator', 'Dynamo']),
            ('Storm Strider', ['Stormweaver', 'Hasted']),
            ('Mirror Image', ['Echoist', 'Soul Conduit']),
            ('Magma Barrier', ['Incendiary', 'Bonebreaker']),
            ('Evocationist', ['Flameweaver', 'Frostweaver', 'Stormweaver']),
            ('Corpse Detonator', ['Necromancer', 'Incendiary']),
            ('Flame Strider', ['Flameweaver', 'Hasted']),
            ('Soul Eater', ['Soul Conduit', 'Necromancer', 'Gargantuan']),
            ('Ice Prison', ['Permafrost', 'Sentinel']),
            ('Frost Strider', ['Frostweaver', 'Hasted']),
            ('Treant Horde', ['Toxic', 'Sentinel', 'Steel-Infused']),
            ('Temporal Bubble', ['Juggernaut', 'Hexer', 'Arcane Buffer']),
            ('Entangler', ['Toxic', 'Bloodletter']),
            ('Drought Bringer', ['Malediction', 'Deadeye']),
            ('Hexer', ['Chaosweaver', 'Echoist']),
            ('Executioner', ['Frenzied', 'Berserker']),
            ('Rejuvenating', ['Gargantuan', 'Vampiric']),
            ('Necromancer', ['Bombardier', 'Overcharged']),
            ('Trickster', ['Overcharged', 'Assassin', 'Echoist']),
            ('Assassin', ['Deadeye', 'Vampiric']),
            ('Empowered Minions', ['Necromancer', 'Executioner', 'Gargantuan']),
            ('Heralding Minions', ['Dynamo', 'Arcane Buffer']),
            ('Arcane Buffer', []),
            ('Berserker', []),
            ('Bloodletter', []),
            ('Bombardier', []),
            ('Bonebreaker', []),
            ('Chaosweaver', []),
            ('Consecrator', []),
            ('Deadeye', []),
            ('Dynamo', []),
            ('Echoist', []),
            ('Flameweaver', []),
            ('Frenzied', []),
            ('Frostweaver', []),
            ('Gargantuan', []),
            ('Hasted', []),
            ('Incendiary', []),
            ('Juggernaut', []),
            ('Malediction', []),
            ('Opulent', []),
            ('Overcharged', []),
            ('Permafrost', []),
            ('Sentinel', []),
            ('Soul Conduit', []),
            ('Steel-Infused', []),
            ('Stormweaver', []),
            ('Toxic', []),
            ('Vampiric', []),
            ('Combo', []),
        ]
        self._images = dict()
        self._update_images(scale)

    def _update_images(self, scale):
        self._scale = scale
        for item, _ in self._arch_items:
            self._images[item] = dict()
            image = self._load_image(item, scale)
            self._image_size = image.size
            self._images[item]['scan-image'] = self._create_scan_image(image)
            # Convert the image to Tk image because we're going to display it
            self._images[item]['display-image'] = ImageTk.PhotoImage(image=image)
            image = image.resize((30, 30))
            self._images[item]['display-small-image'] = ImageTk.PhotoImage(image=image)

    def _load_image(self, item: str, scale: float):
        image = Image.open(f'pictures/{item}.png')
        # Scale the image according to the input parameter
        return image.resize((int(image.width * scale), int(image.height * scale)))

    def _create_scan_image(self, image):
        # Remove alpha channel and replace it with predefined background color
        background = Image.new('RGBA', image.size, (10, 10, 32))
        image_without_alpha = Image.alpha_composite(background, image)
        scan_template = cv2.cvtColor(np.array(image_without_alpha), cv2.COLOR_RGB2BGR)
        w, h, _ = scan_template.shape

        # Crop the image to help with scanning
        return scan_template[int(h * 1.0 / 10):int(h * 2.3 / 3), int(w * 1.0 / 6):int(w * 5.5 / 6)]


    def get_scan_image(self, item):
        return self._images[item]['scan-image']

    def get_display_image(self, item):
        return self._images[item]['display-image']

    def get_display_small_image(self, item):
        return self._images[item]['display-small-image']

    def items(self):
        for item, _ in self._arch_items:
            yield item

    def recipes(self):
        for item, recipe in self._arch_items:
            if recipe:
                yield (item, recipe)

    @property
    def image_size(self):
        return self._image_size

    @property
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, scale: float) -> None:
        self._update_images(scale)


class ImageScanner:
    """
    Implements scanning algorithm with OpenCV. Maintans the scanning window to speed up the scanning.
    """
    def __init__(self, screen_width: int, screen_height: int, items_map: ArchnemesisItemsMap):
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._scanner_window_size = tuple(map(int, [0.1 * screen_height, 0.3 * screen_height, 0.41 * screen_height, 0.41 * screen_height]))
        self._items_map = items_map
        self._confidence_threshold = 0.94

    def scan(self) -> Dict[str, List[Tuple[int, int]]]:
        bbox = (self._scanner_window_size[0], self._scanner_window_size[1], self._scanner_window_size[0] + self._scanner_window_size[2], self._scanner_window_size[1] + self._scanner_window_size[3])
        print('bbox=', bbox)
        screen = ImageGrab.grab(bbox=bbox)
        screen = np.array(screen)
        screen = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        results = dict()

        for item in self._items_map.items():
            heat_map = cv2.matchTemplate(screen, self._items_map.get_scan_image(item), cv2.TM_CCOEFF_NORMED)
            _, confidence, _, (x, y) = cv2.minMaxLoc(heat_map)
            print(f'Best match for {item}: x={x}, y={y} = {confidence}')
            findings = np.where(heat_map >= self._confidence_threshold)
            if len(findings[0]) > 0:
                results[item] = [(findings[1][i], findings[0][i]) for i in range(len(findings[0]))]
        return results

    @property
    def scanner_window_size(self) -> Tuple[int, int, int, int]:
        return self._scanner_window_size

    @scanner_window_size.setter
    def scanner_window_size(self, value: Tuple[int, int, int, int]) -> None:
        self._scanner_window_size = value

    @property
    def confidence_threshold(self) -> float:
        return self._confidence_threshold

    @confidence_threshold.setter
    def confidence_threshold(self, value) -> None:
        self._confidence_threshold = value

    @property
    def screen_width(self) -> int:
        return self._screen_width

    @property
    def screen_height(self) -> int:
        return self._screen_height


class UIOverlay:
    """
    Overlay window using tkinter '-topmost' property
    """
    def __init__(self, root, items_map: ArchnemesisItemsMap, image_scanner: ImageScanner):
        self._items_map = items_map
        self._image_scanner = image_scanner
        self._root = root
        self._scan_results_window = None
        self._highlight_windows_to_show = list()

        self._settings = Settings(root, items_map, image_scanner)
        self._create_controls()

        self._root.configure(bg='')
        self._root.overrideredirect(True)
        self._root.geometry("+5+125")
        self._root.wm_attributes("-topmost", True)
        self._recipes_visible = False
        self._result_visible = False

        self._results = {}
        self._available_recipes = []

    @staticmethod
    def create_toplevel_window(bg=''):
        w = tk.Toplevel()
        w.configure(bg=bg)
        # Hide window outline/controls
        w.overrideredirect(True)
        # Make sure the window is always on top
        w.wm_attributes("-topmost", True)
        return w

    def _create_controls(self) -> None:
        l = tk.Button(self._root, text='[X]', fg=COLOR_FG_GREEN, bg=COLOR_BG, font=FONT_SMALL)
        l.bind('<Button-1>', sys.exit)
        l.grid(row=0, column=0)

        settings = tk.Button(self._root, text='Settings', fg=COLOR_FG_GREEN, bg=COLOR_BG, font=FONT_SMALL)
        settings.bind('<Button-1>', lambda _: self._settings.show())
        settings.grid(row=0, column=1)

        self._scan_label_text = tk.StringVar(self._root, value='Scan')
        self._scan_label = tk.Button(self._root, textvariable=self._scan_label_text, fg=COLOR_FG_GREEN, bg=COLOR_BG, font=FONT_SMALL)
        self._scan_label.bind("<Button-1>", self._scan)
        self._scan_label.grid(row=0, column=2)

        self._toggle_label_text = tk.StringVar(self._root, value='▲')
        self._toggle_label = tk.Button(self._root, textvariable=self._toggle_label_text, fg=COLOR_FG_GREEN, bg=COLOR_BG, font=FONT_SMALL)
        self._toggle_label.bind("<Button-1>", self._toggle)
        self._toggle_label.grid(row=0, column=3)
    
    def _eval(self, combo, inventory):
        recipes = {}
        for result, ingredient in self._items_map.recipes():
            recipes[result] = ingredient
        viable = []
        short = []
        reserved = {}

        def search(item):
            if inventory.get(item):
                loc, inventory[item] = inventory[item][0], inventory[item][1:]
                if len(inventory[item]) == 0:
                    del inventory[item]
                return loc
            elif reserved.get(item):
                loc, reserved[item] = reserved[item][0], reserved[item][1:]
                if len(reserved[item]) == 0:
                    del reserved[item]
                return loc
            elif len(recipes.get(item, [])) > 0:
                locs = [search(x) for x in recipes[item]]
                if all(loc is not None for loc in locs):
                    viable.append((item, [x for x in locs if len(x) > 0], False))
                    return None
                else:
                    for name, loc in zip(recipes[item], locs):
                        if loc is not None:
                            reserved.setdefault(name, [])
                            reserved[name].append(loc)
                        else:
                            short.append(name)
            return None

        if all(inventory.get(i) for i in combo):
            viable.append(('Combo', [inventory[i][0] for i in combo], False))
            for item in combo:
                inventory[item] = inventory[item][1:]
                if len(inventory[item]) == 0:
                    del inventory[item]
        else:
            for item in combo:
                search(item)
        print('Short:', short)
        return viable

    def _scan(self, _) -> None:
        self._scan_label_text.set('Scanning...')
        self._root.update()
        results = self._image_scanner.scan()
        print('Count:', sum(map(lambda x: len(x), results.values())))
        item_list = []
        for name, locs in results.items():
            item_list.extend((loc, name) for loc in locs)
        for loc, name in sorted(item_list):
            print(loc, name)
        if len(results) > 0:
            for item in sorted(results.keys()):
                print(item, results[item])
            available_recipes = []
            for combo in self._settings.combos():
                available_recipes.extend(self._eval(combo, results))
            self._results = results
            self._available_recipes = available_recipes
            if len(self._available_recipes) == 0:
                self._hide(None)
            else:
                self._set_recipes_visible(True, self._settings.should_display_inventory_items())
        else:
            self._results = {}
            self._available_recipes = []
            self._hide(None)
        self._scan_label_text.set('Scan')
    
    def _toggle(self, _) -> None:
        if not self._recipes_visible:
            if len(self._available_recipes) == 0:
                self._set_recipes_visible(True, True)
            else:
                self._set_recipes_visible(True, self._settings.should_display_inventory_items())
        elif not self._result_visible:
            self._set_recipes_visible(True, True)
        else:
            self._set_recipes_visible(False, False)
    
    def _set_recipes_visible(self, recipes_visible, result_visible):
        self._recipes_visible = recipes_visible
        self._result_visible = result_visible

        if self._recipes_visible and self._result_visible:
            self._toggle_label_text.set('▼')
            self._show_scan_results(self._results, self._available_recipes, self._result_visible)
        elif self._recipes_visible:
            self._toggle_label_text.set('-')
            self._show_scan_results(self._results, self._available_recipes, self._result_visible)
        else:
            self._toggle_label_text.set('▲')
            self._hide(None)

    def _hide(self, _) -> None:
        if self._scan_results_window is not None:
            self._scan_results_window.destroy()
        self._clear_highlights(None)

    def _show_scan_results(self, results: Dict[str, List[Tuple[int, int]]], available_recipes: List[Tuple[str, List[Tuple[int, int]], bool]], result_visible: bool) -> None:
        self._hide(None)
        self._recipes_visible = True
        self._results = results
        self._available_recipes = available_recipes
        self._scan_results_window = UIOverlay.create_toplevel_window()
        x = int(self._root.winfo_x())
        y = int(self._root.winfo_y() + self._root.winfo_height())
        self._scan_results_window.geometry(f'+{x}+{y}')

        last_column = 0
        if result_visible:
            last_column = self._show_inventory_list(results)
        self._show_available_recipes_list(available_recipes, last_column + 2)

    def _show_inventory_list(self, results: Dict[str, List[Tuple[int, int]]]) -> int:
        row = 0
        column = 0

        for item in self._items_map.items():
            inventory_items = results.get(item)
            if inventory_items is not None:
                row, column = self._show_image_and_label(item, inventory_items, COLOR_FG_WHITE, f'x{len(inventory_items)} {item}', row, column)
        return column


    def _show_available_recipes_list(self, available_recipes: List[Tuple[str, List[Tuple[int, int]], bool]], column: int) -> None:
        row = 0

        for item, inventory_items, exists_in_inventory in available_recipes:
            if exists_in_inventory:
                fg = COLOR_FG_GREEN
            else:
                fg = COLOR_FG_ORANGE
            row, column = self._show_image_and_label(item, inventory_items, fg, item, row, column)

    def _show_image_and_label(self, item, inventory_items: Tuple[int, int], highlight_color: str, label_text: str, row: int, column: int) -> Tuple[int, int]:
        image = tk.Label(self._scan_results_window, image=self._items_map.get_display_small_image(item), bg=COLOR_BG, pady=5)
        image.bind('<Enter>', lambda _, arg=inventory_items, color=highlight_color: self._highlight_items_in_inventory(arg, color))
        image.bind('<Leave>', self._clear_highlights)
        image.grid(row=row, column=column)
        tk.Label(self._scan_results_window, text=label_text, font=FONT_BIG, fg=highlight_color, bg=COLOR_BG).grid(row=row, column=column + 1, sticky='w', padx=5)
        row += 1
        if row % 8 == 0:
            column += 2
            row = 0
        return (row, column)

    def _highlight_items_in_inventory(self, inventory_items: List[Tuple[int, int]], color: str) -> None:
        self._highlight_windows_to_show = list()
        for (x, y) in inventory_items:
            x_offset, y_offset, _, _ = self._image_scanner.scanner_window_size
            x += x_offset
            y += y_offset
            width = int(self._items_map.image_size[0] * 0.7)
            height = int(self._items_map.image_size[1] * 0.7)
            w = UIOverlay.create_toplevel_window(bg=color)
            w.geometry(f'{width}x{height}+{x}+{y}')
            self._highlight_windows_to_show.append(w)

    def _clear_highlights(self, _) -> None:
        for w in self._highlight_windows_to_show:
            w.destroy()

    def run(self) -> None:
        self._root.mainloop()


class Settings:
    def __init__(self, root, items_map, image_scanner):
        self._root = root
        self._items_map = items_map
        self._image_scanner = image_scanner

        self._config = ConfigParser()
        self._config_file = 'settings.ini'

        self._config.read(self._config_file)
        if 'settings' not in self._config:
            self._config.add_section('settings')
        s = self._config['settings']

        scanner_window_size = s.get('scanner_window')
        if scanner_window_size is not None:
            self._image_scanner.scanner_window_size = tuple(map(int, scanner_window_size.replace('(', '').replace(')', '').replace(',', '').split()))
        self._items_map.scale = float(s.get('image_scale', self._items_map.scale))
        self._image_scanner.confidence_threshold = float(s.get('confidence_threshold', self._image_scanner.confidence_threshold))
        b = s.get('display_inventory_items')
        self._display_inventory_items = True if b is not None and b == 'True' else False
        if s.get('combos') is None:
            self._combos = [
            ['Innocence-Touched', 'Brine King-Touched', 'Kitava-Touched', 'Treant Horde'],
            ['Mirror Image', 'Assassin', 'Rejuvenating', 'Treant Horde'],
            ['Innocence-Touched', 'Brine King-Touched', 'Kitava-Touched', 'Treant Horde'],
            ['Arakaali-Touched', 'Brine King-Touched', 'Effigy', 'Treant Horde']
        ]
        else:
            self._combos = json.loads(s.get('combos'))

    def show(self) -> None:
        self._window = tk.Toplevel()

        self._window.geometry('+100+200')
        self._window.protocol('WM_DELETE_WINDOW', self._close)

        current_scanner_window = f'{self._image_scanner.scanner_window_size}'.replace('(', '').replace(')', '')
        v = tk.StringVar(self._window, value=current_scanner_window)
        self._scanner_window_entry = tk.Entry(self._window, textvariable=v)
        self._scanner_window_entry.grid(row=0, column=0)
        tk.Button(self._window, text='Set scanner window', command=self._update_scanner_window).grid(row=0, column=1)

        v = tk.DoubleVar(self._window, value=self._items_map.scale)
        self._scale_entry = tk.Entry(self._window, textvariable=v)
        self._scale_entry.grid(row=1, column=0)
        tk.Button(self._window, text='Set image scale', command=self._update_scale).grid(row=1, column=1)

        v = tk.DoubleVar(self._window, value=self._image_scanner.confidence_threshold)
        self._confidence_threshold_entry = tk.Entry(self._window, textvariable=v)
        self._confidence_threshold_entry.grid(row=2, column=0)
        tk.Button(self._window, text='Set confidence threshold', command=self._update_confidence_threshold).grid(row=2, column=1)

        c = tk.Checkbutton(self._window, text='Display inventory items', command=self._update_display_inventory_items)
        c.grid(row=3, column=0)
        if self._display_inventory_items:
            c.select()

    def _close(self) -> None:
        self._window.destroy()

    def _save_config(self) -> None:
        self._config['settings']['scanner_window'] = str(self._image_scanner.scanner_window_size)
        self._config['settings']['image_scale'] = str(self._items_map.scale)
        self._config['settings']['confidence_threshold'] = str(self._image_scanner.confidence_threshold)
        self._config['settings']['combos'] = json.dumps(self._combos)
        self._config['settings']['display_inventory_items'] = str(self._display_inventory_items)
        with open(self._config_file, 'w') as f:
            self._config.write(f)

    def _update_scanner_window(self) -> None:
        try:
            x, y, width, height = map(int, self._scanner_window_entry.get().replace(',', '').split())
        except ValueError:
            print('Unable to parse scanner window parameters')
            return

        scanner_window_to_show = UIOverlay.create_toplevel_window(bg='white')
        scanner_window_to_show.geometry(f'{width}x{height}+{x}+{y}')
        self._image_scanner.scanner_window_size = (x, y, width, height)
        scanner_window_to_show.after(200, scanner_window_to_show.destroy)
        self._save_config()

    def _update_scale(self) -> None:
        try:
            new_scale = float(self._scale_entry.get())
        except ValueError:
            print('Unable to parse image scale parameter')
            return
        self._items_map.scale = new_scale
        self._save_config()

    def _update_confidence_threshold(self) -> None:
        try:
            new_threshold = float(self._confidence_threshold_entry.get())
        except ValueError:
            print('Unable to parse confidence threshold parameter')
            return
        self._image_scanner.confidence_threshold = new_threshold
        self._save_config()

    def _update_display_inventory_items(self) -> None:
        self._display_inventory_items = not self._display_inventory_items
        self._save_config()

    def should_display_inventory_items(self) -> bool:
        return self._display_inventory_items

    def combos(self):
        return self._combos

def calculate_default_scale(screen_width: int, screen_height: int) -> float:
    """
    TODO: validate the math for non 16:9 resolutions (e.g. ultrawide monitors)
    """

    # Assume that all source images have 78x78 size
    source_image_height = 78.0

    # Take 0.90 as a golden standard for 2560x1440 resolution and calculate
    # scales for other resolutions based on that
    constant = 1440.0 / (source_image_height * 0.91)
    scale = screen_height / (source_image_height * constant)

    return scale


def tk_main():
    # Create root as early as possible to initialize some modules (e.g. ImageTk)
    root = tk.Tk()

    # There are probably better ways to get screen resoultions but I'm lazy
    screen = ImageGrab.grab()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.size

    items_map = ArchnemesisItemsMap(calculate_default_scale(SCREEN_WIDTH, SCREEN_HEIGHT))

    image_scanner = ImageScanner(SCREEN_WIDTH, SCREEN_HEIGHT, items_map)

    overlay = UIOverlay(root, items_map, image_scanner)
    overlay.run()

def main():
    PATH = os.path.join(os.getenv('UserProfile'), r'Documents\My Games\Path of Exile\Screenshots')
    print(ImageGrab.grab().size)

    root = tk.Tk()
    latest_img = os.path.join(PATH, max(os.listdir(PATH), key=lambda fn: int(fn[11:-4])))
    with Image.open(latest_img) as screen:
        SCREEN_WIDTH, SCREEN_HEIGHT = screen.size
        items_map = ArchnemesisItemsMap(calculate_default_scale(SCREEN_WIDTH, SCREEN_HEIGHT))
        image_scanner = ImageScanner(screen.crop(AREA), items_map)
        result = image_scanner.scan()
        print(result)
        items = []
        for name in result.keys():
            items = items + [[loc[0], loc[1], name] for loc in result[name]]
        for i in sorted(items):
            print(i)
        print('Count:', sum(map(lambda x: len(x), result.values())))
        result = dict([x, len(result[x])] for x in result.keys() if len(result[x]) > 0)
        combos = [
            ['Innocence-Touched', 'Brine King-Touched', 'Kitava-Touched', 'Treant Horde'],
            ['Innocence-Touched', 'Brine King-Touched', 'Kitava-Touched', 'Treant Horde'],
            ['Mirror Image', 'Assassin', 'Rejuvenating', 'Treant Horde'],
            ['Mirror Image', 'Assassin', 'Rejuvenating', 'Treant Horde'],
            ['Arakaali-Touched', 'Brine King-Touched', 'Effigy', 'Treant Horde']
        ]
        recipe = 1
        while recipe > 0:
            recipe = 0
            for combo in combos:
                recipe += items_map.eval(combo, result)
        for item, count in sorted([(x, result[x]) for x in result.keys()]):
            print(item, count)

tk_main()