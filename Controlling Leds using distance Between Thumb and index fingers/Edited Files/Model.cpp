#include <gui/model/Model.hpp>
#include <gui/model/ModelListener.hpp>

#ifndef SIMULATOR
#include "main.h"
#include "cmsis_os2.h"
#include <cstring>
extern "C"
{
	extern osMessageQueueId_t uartQueueHandle;
	extern uint8_t rxData2[11];

}

#endif
Model::Model() : modelListener(0)
{

}

void Model::tick()
{
#ifndef SIMULATOR
	if(osMessageQueueGetCount(uartQueueHandle) > 0)
	{
		modelListener-> uartData((char *)rxData2);
	}

#endif
}
