#pragma once

/**
 * Author Ivo Blöchliger
 */

#include <Adafruit_NeoPixel.h>

#define MCP_SDA 23
#define MCP_SCL 22
#define MCP_ADDR 0x20


class TetrisTable {
    public:
    
    /**
     * Initialized the Neopixels, Buttons and Leds
     */
    bool begin();

    /**
     * Sets a pixel without showing it
     * You can compute color values with the color-function
     */
    void setPixel(int x, int y, uint32_t color);
    /**
     * Converts rgb to a color code usable in SetPixel
     */
    uint32_t color(uint8_t r, uint8_t g, uint8_t b);
    /**
     * Displays all pixels (refresh)
     */
    void show();

    /**
     * Sets the state of the button LEDs
     * @param leds: Bitmap with 8 Bits 0=off, 1=on
     */
    void setButtonLEDs(uint8_t leds);
    /**
     * Gets the state of the button LEDs
     * @returns state (Bitmap with 8 Bits)
     */
    uint8_t getButtonLEDs();
    /**
     * @returns the state of the buttons as a Bitmap of 8 bits.
     * 0 means not pressed, 1 means pressed
     */
    uint8_t getButtons();

    // The Neopixels Object
    Adafruit_NeoPixel *pixels = nullptr;

    // Paint ASCII-character
    void paintChar(int x, int y, char c, uint32_t color, int bg_color=-1);
    void paintString(int x, int y, const char *s, uint32_t color, int bg_color=-1);

    private:
    uint8_t ledState = 0;

};
