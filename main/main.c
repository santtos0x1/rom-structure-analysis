#include <stdio.h>
#include "driver/gpio.h"
#include <stdint.h>
#include "esp_rom_sys.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define A0_PIN  4
#define A1_PIN  5
#define A2_PIN  12
#define A3_PIN  13
#define A4_PIN  14
#define A5_PIN  16
#define A6_PIN  17
#define A7_PIN  18
#define A8_PIN  19
#define A9_PIN  21
#define A10_PIN 22
#define A11_PIN 23

#define D0_PIN  25
#define D1_PIN  26
#define D2_PIN  27
#define D3_PIN  32
#define D4_PIN  33
#define D5_PIN  34
#define D6_PIN  35
#define D7_PIN  36

gpio_config_t io_conf = {
    .pin_bit_mask = (1ULL<<A0_PIN) | (1ULL<<A1_PIN) | (1ULL<<A2_PIN) | 
                    (1ULL<<A3_PIN) | (1ULL<<A4_PIN) | (1ULL<<A5_PIN) | 
                    (1ULL<<A6_PIN) | (1ULL<<A7_PIN) | (1ULL<<A8_PIN) | 
                    (1ULL<<A9_PIN) | (1ULL<<A10_PIN) | (1ULL<<A11_PIN),
    .mode = GPIO_MODE_OUTPUT,
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .pull_up_en = GPIO_PULLUP_DISABLE,
    .intr_type = GPIO_INTR_DISABLE
};

gpio_config_t d_io_conf = {
    .pin_bit_mask = (1ULL<<D0_PIN) | (1ULL<<D1_PIN) | (1ULL<<D2_PIN) | 
                    (1ULL<<D3_PIN) | (1ULL<<D4_PIN) | (1ULL<<D5_PIN) | 
                    (1ULL<<D6_PIN) | (1ULL<<D7_PIN),
    .mode = GPIO_MODE_INPUT,
    .pull_down_en = GPIO_PULLDOWN_DISABLE,
    .pull_up_en = GPIO_PULLUP_DISABLE,
    .intr_type = GPIO_INTR_DISABLE
};

void vTaskCode(void *pvParameters){
    uint16_t counter = 0;
    uint32_t bit;
    uint16_t d_data;
    uint16_t rom_addr;

    vTaskDelay(pdMS_TO_TICKS(2000));
    
    printf("ADDR,DATA\n");
    for(;;)
    {
        rom_addr = 0;
        d_data = 0;
        // Show
        for(int i = 11; i >= 0; i--)
        {
            bit = (counter >> i) & 1;
            
            rom_addr = counter;

            switch(i)
            {
                case 0:  gpio_set_level((gpio_num_t)A0_PIN, (uint32_t)bit);  break;
                case 1:  gpio_set_level((gpio_num_t)A1_PIN, (uint32_t)bit);  break;
                case 2:  gpio_set_level((gpio_num_t)A2_PIN, (uint32_t)bit);  break;
                case 3:  gpio_set_level((gpio_num_t)A3_PIN, (uint32_t)bit);  break;
                case 4:  gpio_set_level((gpio_num_t)A4_PIN, (uint32_t)bit);  break;
                case 5:  gpio_set_level((gpio_num_t)A5_PIN, (uint32_t)bit);  break;
                case 6:  gpio_set_level((gpio_num_t)A6_PIN, (uint32_t)bit);  break;
                case 7:  gpio_set_level((gpio_num_t)A7_PIN, (uint32_t)bit);  break;
                case 8:  gpio_set_level((gpio_num_t)A8_PIN, (uint32_t)bit);  break;
                case 9:  gpio_set_level((gpio_num_t)A9_PIN, (uint32_t)bit);  break;
                case 10: gpio_set_level((gpio_num_t)A10_PIN, (uint32_t)bit); break;
                case 11: gpio_set_level((gpio_num_t)A11_PIN, (uint32_t)bit); break;
                default: break;
            }
        }

        for(int i = 7; i >= 0; i--)
        {
            switch (i)
            {
                case 0: d_data |= (gpio_get_level((gpio_num_t)D0_PIN) << i); break;
                case 1: d_data |= (gpio_get_level((gpio_num_t)D1_PIN) << i); break;
                case 2: d_data |= (gpio_get_level((gpio_num_t)D2_PIN) << i); break;
                case 3: d_data |= (gpio_get_level((gpio_num_t)D3_PIN) << i); break;
                case 4: d_data |= (gpio_get_level((gpio_num_t)D4_PIN) << i); break;
                case 5: d_data |= (gpio_get_level((gpio_num_t)D5_PIN) << i); break;
                case 6: d_data |= (gpio_get_level((gpio_num_t)D6_PIN) << i); break;
                case 7: d_data |= (gpio_get_level((gpio_num_t)D7_PIN) << i); break;
                default: break;
            }
        }

        printf("0x%03X,0x%02X\n", rom_addr, d_data);

        vTaskDelay(pdMS_TO_TICKS(100));
        counter++;
        if (counter > 4095) {
            counter = 0;
        }
    }
}

void app_main(void)
{
    gpio_config(&io_conf);
    gpio_config(&d_io_conf);

    xTaskCreate(vTaskCode, "TASK", 4096, NULL, 5, NULL);   
}