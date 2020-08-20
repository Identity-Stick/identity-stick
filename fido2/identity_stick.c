// Copyright 2020 Identity Stick Developers
//
// Licensed under the Apache License, Version 2.0, <LICENSE-APACHE or
// http://apache.org/licenses/LICENSE-2.0> or the MIT license <LICENSE-MIT or
// http://opensource.org/licenses/MIT>, at your option. This file may not be
// copied, modified, or distributed except according to those terms.
#include "identity_stick.h"
#include "log.h"

#define IDSTICKPARTLENGTH 20
#define STICKNAME 0x03
#define STICKFIRSTNAME 0x04
#define STICKBIRTHDATE 0x0E
#define IDSTICKERROR 0x01

const char AVAILABLE_DATA[] =  "{\"available-data\": [\"n-fN\",\"n-gN\",\"bD\"], \"pub_key\": \"test.de\"}";
const char IDSTICKNAME[] = "{\"value\": \"Palpatine\", \"hash\": \"e890d7f1b82678308d955b2e867147c560f78e68463952ee45d0adb5de243a34\", \"sign\": \"0a5c9294e48f27815a3991aa1b4f7cbd7edc5c485125bda8644b07de1686bdab8d36935b786e98681f395fa53bf1f774cf0008b397b8795d3dc3995913430d8dbb72b7dbf2cfe245724965474d0d09231486c1d14dafb35e76042bb0486a59515c16951a98d46a8869da80aedcdcf2475ea6fdddf6fe78d9c964c8239034d5938177068e047e2601e03d9982b7e536d81e232bf9ebdd4552109976642718f65cd4d167e4ae91f1bc616d3470350ef3e75cd2bc428731838115e854a548d267b9fff0f1ae7eb60e7f0fbc866f712b859f71e7c24b1800154621749ef9b225d80b02a89cd92b6444c1b0bcc89a7371e40af46c87d6d4c58c65631851fbd1080e73d5b1d58b4f635fd0a0e2345274a6643b87cd25c2e1eb24374318dc7664dc4c325b44128c5a0f7d79414ebdd6620027f65ffaf2c37efa6d4463da46d9ca8eac77a968967899042a42f2d761da0ca79ab85c448198c758786ce20fbfdd2dc58c232e7f8071882f8923ba99875873233e662a29fbd915d8af2ba7cad5dd6e04205c6350d5e7f98da0d08d3bd6a842237787a24e2cb2823b0120afa24ece19d40a7d0dcd8f8fbebe9e20e4a7a94902c19f8c43f9a444fe07d8ad890cc974ed7dfa6bc78d6be72c812f31426f50a2f7b6cea43c5f8f636a205b1426ccaa8704e0381121c96201d4727a9920164e162f90c98ed91ba3b65bbe3128a2cc0b6dbf5f5f49\"}";
const char IDSTICKFIRSTNAME[] = "{\"value\": \"Rey\", \"hash\": \"3ae8144bc9465782e520cbf4a5ced15ac3cd31f122842ca6f23cf40320d28240\", \"sign\": \"837696a40577ef952c6972d0b2b6c26854cadfe59c58e18dcbb97cab1b171dfcd4ab7eea15a8f371aeab7f92d821c91cbe13c7f54cf02734b887b1ff0d59870c513c9c9592cf61b27a743dca1d74bd0845af616c62e5b68ad15bbbc2321781efec8cffcbb8110bfdaa13b0712d768f7c115e4f336828fa52b639b04195f932e3e5f0376d48a61a139507a93604a882006742901b0cd9afcece623ed2cb8b0987b2dbc9d79aae3589da899e2be067c8a49fe33684407e22864ead6359858340baf4ad804dab52cb0fed9498748a70d8fefdb091ec53721cd202215197ffb443ea7917a7b6390c4427582ecfedf51b0a9670e9b379272828e2f2391becced5efda6a09288ea50a7771a61e97efcc70098459975ae1ba50101ceaeef31ba8a1b8fb1b11a9e79bfb9eab78b8ca5cafac8e244bb5a1aa8af69d1e2b471f3e70d7cc95535bfdb93ab73f48b55657f8e05a20a7025ff08e8d6d5e310f19a30fdeab7ed3ae33177dfa53d42dd9b5a89951316aae3f3484a2fff5343c4595e6bf2098260519ed1a2cd65e5703fa4e221f9678fcfb6872bd323dc383490859908f689733a42bc93af5997cfef46196d2472eb71272d17ed9bcaf91b7b96bcb7231d2885a450150e0ad7ad3c178df277ba0d4df1dfc809b44c3b0d727a62471227a2c76f9e0776ff48d2012f6eceb5e51f78959f328bb90fcf5421e7081bcfed44381b00b41\"}";
const char IDSTICKBIRTHDATE[] = "{\"value\": \"2015-12-17\", \"hash\": \"9b0af8568bd1320e299706c8ad4bf4d27fdcc07b3dfedaeb047181c615ba48cc\", \"sign\": \"09c88e7c485474d62a7c883ff6a9c7fe06b8678eaa64035e72033092bdbc5045fa8e633d07052dd3338bf6f4929c3b29e08e92764ad08d6db946996fed3ee200b68762feb0a6fc24119ccde201a260a2643ffc57f2659ab14e68f1064243cdf7b7922954e7a7035d4179ae390b7a29411a7ba3f26de68bbb004b7fe904042c1905cd383c763c0cce6b67697926860b889fae1b44eb593981d6df179a8b02fb323a8809f731ace279c5b99c8623e9cb0e5bae1a6f90218f67d80ff0dd3e89e8d0ff31e4fa3332c9c098181046a7aac936d9cd1c976404be4c2a19b0a78a9dd433639c2f2f4f29d64665e6c216ebdff6fcf814bbd227f933137bbab8294a0bc7803c6c395a9f27e2bc45d14b4f6c5cbd844f96137727f6f628e5f9d97fadff25c05a02ff68850a4cba06c815a9ebf26d8a79bb7ffa896267506ff810833bad7e5eb318f11c796fe937889a216d30da52c4463c23e63f28d90cf9230d20c2fceedbd52aea8c78ab0bb75bff08f798fb16c4396eed517c0c110daec77d88149160914185361b7f59bb5d5130758d5b27b21cf1d006460619d801cc500536bd234a976dc0b2d82e9a4cfde1414b0918a00c1d658aee714de94868627879bd662ca1df0d99e1d2801b33caee194e37c29008b220e50e720f196f42c3f0d9b228c54ecf2999c9c5012ce7f70cccbfe02159c6a876da29babc63b098810ab2ee26d1567f\"}";

int getAvailableData(char * dest){
	strncpy(dest, &AVAILABLE_DATA[0], strlen(AVAILABLE_DATA) + 1);
	
	return 0;
}

int nextString(const char* type, int number, char * nextString, int len){
	if (len < IDSTICKPARTLENGTH){
		return IDSTICKERROR;
	}
	size_t offset = number * IDSTICKPARTLENGTH;
	int ret = 0;
	
	if(strcmp(type, "n-gN") == 0) {
        ret = safeStrCopyFromConstant(nextString, IDSTICKNAME, IDSTICKPARTLENGTH, offset);
    }else if(strcmp(type, "n-fN") == 0) {
        ret = safeStrCopyFromConstant(nextString, IDSTICKFIRSTNAME, IDSTICKPARTLENGTH, offset);
    }else if(strcmp(type, "bD") == 0) {
    	ret = safeStrCopyFromConstant(nextString, IDSTICKBIRTHDATE, IDSTICKPARTLENGTH, offset);
    }else{
        return IDSTICKERROR;
    }
	
	return ret;	
}

int safeStrCopyFromConstant(char * dest, const char * origin, int len, size_t offset){
	int copyLength = len;
	//TODO: make comparison type safe
	if(strlen(origin) < offset + len){
		if(strlen(origin) > offset){
			copyLength = strlen(origin) - offset;	
		}else{
			return 1;
		}
	}
	strncpy(dest, &origin[offset], copyLength);
	dest[copyLength] = '\0';

	return 0;
}

int getPartLength(){
	return IDSTICKPARTLENGTH;
}

int lenRequestedString(const char * type){
	if(strcmp(type, "n-gN") == 0) {
        if(strlen(IDSTICKNAME) % IDSTICKPARTLENGTH != 0){
			return strlen(IDSTICKNAME)/IDSTICKPARTLENGTH + 1;
		}
		return strlen(IDSTICKNAME)/IDSTICKPARTLENGTH;
    }else if(strcmp(type, "n-fN") == 0) {
        if(strlen(IDSTICKFIRSTNAME) % IDSTICKPARTLENGTH != 0){
			return strlen(IDSTICKFIRSTNAME)/IDSTICKPARTLENGTH + 1;
		}
		return strlen(IDSTICKFIRSTNAME)/IDSTICKPARTLENGTH;
    }else if(strcmp(type, "bD") == 0) {
        if(strlen(IDSTICKBIRTHDATE) % IDSTICKPARTLENGTH != 0){
			return strlen(IDSTICKBIRTHDATE)/IDSTICKPARTLENGTH + 1;
		}
		return strlen(IDSTICKBIRTHDATE)/IDSTICKPARTLENGTH;
    }else{
        return -1;
    } 	
}

bool isValidAttribute(const char * type){
	if(strcmp(type, "n-gN") == 0) {
        return true;
    }else if(strcmp(type, "n-fN") == 0) {
        return true;
    }else if(strcmp(type, "bD") == 0) {
        return true;
    }else{
        return false;
    } 	
}