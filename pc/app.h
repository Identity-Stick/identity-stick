/*
 * app.h
 *
 *  Created on: Jun 26, 2018
 *      Author: conor
 */

#ifndef SRC_APP_H_
#define SRC_APP_H_

#define USING_DEV_BOARD

#define USING_PC

#define DEBUG_LEVEL 1

#define ENABLE_U2F

//#define BRIDGE_TO_WALLET

void printing_init();

//                              0xRRGGBB
#define LED_INIT_VALUE			0x000800
#define LED_WINK_VALUE			0x000008
#define LED_MAX_SCALER          30
#define LED_MIN_SCALER          1
// # of ms between each change in LED
#define HEARTBEAT_PERIOD        100
// Each LED channel will be multiplied by a integer between LED_MAX_SCALER
// and LED_MIN_SCALER to cause the slow pulse.  E.g.
// #define LED_INIT_VALUE			0x301000
// #define LED_MAX_SCALER          30
// #define LED_MIN_SCALER          1
// #define HEARTBEAT_PERIOD        8
// Will pulse from 0x301000 to 0x903000 to 0x301000 ...
// Which will take ~8 * (30)*2 ms


#endif /* SRC_APP_H_ */
