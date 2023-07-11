# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger

mod = "mod4"
terminal = "kitty"

def addSection(
    qtile,
    prompt: str = "AddSection: ",
    widget: str = "prompt",
    command: str = "%s",
    complete: str = "cmd",
    shell: bool = True,
    aliases: dict[str, str] | None = None,
) -> None:
    def f(args: str) -> None:
        if args:
            if aliases and args in aliases:
                args = aliases[args]
            cc = "qtile cmd-obj -o layout -f add_section -a "+args
            qtile.cmd_spawn(cc)
    mb = qtile.widgets_map[widget]
    mb.start_input(prompt, f, complete)

def delSection(
    qtile,
    prompt: str = "DelSection: ",
    widget: str = "prompt",
    command: str = "%s",
    complete: str = "cmd",
    shell: bool = True,
    aliases: dict[str, str] | None = None,
) -> None:
    def f(args: str) -> None:
        if args:
            if aliases and args in aliases:
                args = aliases[args]
            cc = "qtile cmd-obj -o layout -f del_section -a "+args
            qtile.cmd_spawn(cc)
    mb = qtile.widgets_map[widget]
    mb.start_input(prompt, f, complete)


keys = [
    #basic movements
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),

    #Moving windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    #Resizing windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    #columns
    Key([mod, "control"], "o", lazy.layout.swap_column_left().when(layout='columns'), desc = "swap column left when columns"),
    Key([mod, "control"], "p", lazy.layout.swap_column_right().when(layout='columns'), desc = "swap column right when columns"),

    #monadtall
    Key([mod, "control"], "f", lazy.layout.grow().when(layout='monadtall'), desc = "grow when monadtall"),
    Key([mod, "control"], "v", lazy.layout.shrink().when(layout='monadtall'), desc = "shrink when monadtall"),
    Key([mod, "control"], "g", lazy.layout.grow_main().when(layout='monadtall'), desc = "grow main when monadtall"),
    Key([mod, "control"], "b", lazy.layout.shrink_main().when(layout='monadtall'), desc = "shrink main when monadtall"),

    Key([mod, "control"], "n", lazy.layout.normalize().when(layout='monadtall'), desc = "normalize when monadtall"),
    Key([mod, "control"], "space", lazy.layout.flip().when(layout='monadtall'), desc = "flip when monadtall"),

    #treetab
    Key([mod], "a", lazy.function(addSection).when(layout='treetab'), desc = "add section when treetab"),
    Key([mod], "d", lazy.function(delSection).when(layout='treetab'), desc = "delete section when treetab"),
    Key([mod], "e", lazy.layout.expand_branch().when(layout='treetab'), desc = "expand branch when treetab"),
    Key([mod], "c", lazy.layout.collapse_branch().when(layout='treetab'), desc = "collapse branch when treetab"),
    Key([mod, "shift"], "p", lazy.layout.move_right().when(layout='treetab'), desc = "move right when treetab"),
    Key([mod, "shift"], "o", lazy.layout.move_left().when(layout='treetab'), desc = "move left when treetab"),
    Key([mod, "shift"], "u", lazy.layout.move_up().when(layout='treetab'), desc = "move up when treetab"),
    Key([mod, "shift"], "m", lazy.layout.move_down().when(layout='treetab'), desc = "move down when treetab"),
    Key([mod, "control"], "u", lazy.layout.section_up().when(layout='treetab'), desc = "section up when treetab"),
    Key([mod, "control"], "m", lazy.layout.section_down().when(layout='treetab'), desc = "section down when treetab"),

    #special keys
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5"), desc="brightness increase"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5-"), desc="brightness decrease"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute alsa_output.pci-0000_04_00.6.analog-stereo toggle"), desc="autio mute toggle"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute alsa_output.pci-0000_04_00.6.analog-stereo toggle"), desc="autio mute toggle"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume alsa_output.pci-0000_04_00.6.analog-stereo +4%"), desc="autio mute toggle"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume alsa_output.pci-0000_04_00.6.analog-stereo -4%"), desc="autio mute toggle"),



    Key([mod, "control"], "f", lazy.window.toggle_fullscreen(), desc = "test"),

    Key([mod], "p", lazy.screen.next_group(), desc="Move to the right group"),
    Key([mod], "o", lazy.screen.prev_group(), desc="Move to the left group"),
    Key([mod], "space", lazy.screen.toggle_group(), desc="Move window focus to other window"),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "i", lazy.next_layout(), desc="Next layouts"),
    Key([mod], "u", lazy.prev_layout(), desc="Previous layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )

layouts = [
    layout.TreeTab(
        border_width = 5,
        fontsize = 18,
        panel_width = 150,
        section_fontsize = 24,
        section_left = 00,
        sections = ['iNsTaNcE'],
        bg_color = "070C02",
        place_right = True,
        padding_left = 0,
        level_shift = 19,
        vspace = 0,
    ),
    layout.Columns(
        border_focus = "d3d3d3",
        border_focus_stack = "8a9a5b",
        border_normal = "000000",
        border_normal_stack = "000000",
        border_width = 5,
        border_on_single = True,
    ),
    layout.MonadTall(
        border_focus = "d3d3d3",
        border_focus_stack = "8a9a5b",
        border_normal = "000000",
        border_normal_stack = "000000",
        border_width = 5,
        border_on_single = True,
        ratio = 0.7,
    ),
]

widget_defaults = dict(
    font="sans",
    fontsize=18,
    padding=9,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(
                    background = "333333",
                    foreground = "FFFFFF",
                    padding = 2,
                ),
                widget.CurrentLayout(
                    background = "d0d0d0",
                    foreground = "000000",
                    padding = 7,
                ),
                widget.GroupBox(
                    background = "222222",
                    foreground = "FFFFFF",
                    padding = 2,
                    disable_drag = True,
                    font = "fira code semibold",
                    highlight_method = "block",
                ),
                widget.Prompt(
                ),

                #later
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Spacer(
                    background = "444444",
                ),

                widget.Pomodoro(
                    background = "d0d0d0",
                    foreground = "000000",
                    color_active = "0000ff",
                    color_break = "000000",
                    color_inactive = "000000",
                    length_long_break = 15,
                    length_pomodori = 25,
                    length_short_break = 5,
                    prefix_inactive = "DoRO",
                    prefix_active = "A: ",
                    prefix_long_break = "B: ",
                    prefix_paused = "pAuSE",
                ),
                widget.Clock(
                    background = "333333",
                    foreground = "FFFFFF",
                    format = "%H:%M  %a %Y-%m-%d",
                ),
                widget.Net(
                    background = "d0d0d0",
                    foreground = "000000",
                    fmt = "nEt: {}",
                    format = '{down}↓↑{up}',
                ),
                widget.CPU(
                    background = "333333",
                    foreground = "FFFFFF",
                ),
                widget.Memory(
                    background = "d0d0d0",
                    foreground = "000000",
                    measure_mem = 'G',
                    fmt = "mEmoRY: {}",
                    format = "{MemUsed:.0f}{mm}",
                ),
                widget.Wlan(
                    background = "333333",
                    foreground = "FFFFFF",
                    fmt = "wIfI: {}",
                    format = "{essid}",
                    interface = "wlo1",
                    update_interval = 1,
                ),
                widget.PulseVolume(
                    background = "d0d0d0",
                    foreground = "000000",
                    fmt = "pUlSE: {}",
                ),
                widget.Backlight(
                    backlight_name = "amdgpu_bl0",
                    change_command = "brightnessctl set {}%",
                    background = "333333",
                    foreground = "FFFFFF",
                    fmt = "bRiGhTnEsS: {}",
                    step = 10,
                    max_chars = 4,
                ),
                widget.Battery(
                    background = "d0d0d0",
                    foreground = "000000",
                    charge_char = "C",
                    discharge_char = "D",
                    format = "{percent:2.0%} {char}",
                    fmt = "bAtTeRY: {}",
                    low_percentage = 0.2,
                    low_background = "FF0000",
                    low_foreground = "000000",
                    update_interval = 10,
                ),
            ],
            22,
            border_width=[0, 0, 1, 0],  # Draw top and bottom borders
        ),
        #wallpaper = "~/Downloads/two.png",
        #wallpaper_mode = "fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

auto_minimize = True

wl_input_rules = None

wmname = "LG3D"
