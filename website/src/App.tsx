import { Button, Flex, Heading, IconButton, Spinner, Text, useColorMode, useToast } from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { FaArrowLeft, FaMicrochip, FaRaspberryPi, FaRegMoon, FaRegSun } from 'react-icons/fa';
import ToggleEverything from './components/ToggleEverything';
import { getBaseUrl } from './components/tools';
import Device from './Device';
import { DeviceList } from './interfaces/DeviceList';

function insertUrlParam(key: string, value: string | undefined, title = '', preserve_hash = false) {
    let searchParams = new URLSearchParams(window.location.search);
    searchParams.set(key, value ?? "");
    let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname
        + value ? '?' + searchParams.toString() : "";
    if (preserve_hash) newurl = newurl + window.location.hash;
    let oldTitle = document.title;
    if (title !== '') {
        window.history.replaceState({ path: newurl }, title, newurl);
        if (document.title !== title) { // fallback if above doesn't work
            document.title = title;
        }
    } else { // in case browsers ever clear titles set with empty string
        window.history.replaceState({ path: newurl }, oldTitle, newurl);
    }
}

function App() {
    const [deviceList, setDeviceList] = useState<DeviceList | undefined>(undefined);
    const [update, setUpdate] = useState(() => Math.random())
    const [currDevice, setCurrDevice] = useState<string | undefined>(undefined)
    const toast = useToast()
    const { colorMode, toggleColorMode } = useColorMode()
    const base = getBaseUrl(window.location)
    const updateDevices = (dev: string | undefined) => {
        if (dev)
            insertUrlParam("id", dev)
        else
            insertUrlParam("id", undefined)
    }

    const baseElements = <Flex justifyContent='center' alignItems='center' w='100%'>
        <Flex flex='1' justifyContent='center' alignItems='center'>
            <FaRaspberryPi style={{ width: '4rem', height: '4rem' }} />
            <Heading className='title'>Raspberry PI Visualizer</Heading>
        </Flex>
        <IconButton mr={4} aria-label="Toggle Mode" onClick={toggleColorMode}>
            {colorMode === 'light' ? <FaRegMoon /> : <FaRegSun />}
        </IconButton>
    </Flex>

    useEffect(() => {
        const params = (new URL(window.location.href)).searchParams
        const device = params.get("id")

        console.log("Device query param is", device)
        if (!device)
            return

        setCurrDevice(device)
        updateDevices(device)
    }, [])

    useEffect(() => {
        const fetchProm = (url: string) => fetch(url).then(e => e.json())
        const deviceList = `${base}/devices/list`

        Promise.all([
            fetchProm(deviceList)
        ])
            .then(([deviceList]) => setDeviceList(deviceList))
            .catch(e => {
                toast({
                    title: "Error",
                    description: "Could not list devices",
                    status: "error"
                })
                console.error(e)
                setTimeout(() => setUpdate(() => Math.random()), 1000)
            })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [update])


    if (currDevice)
        return <>
            {baseElements}
            <Flex mt='5'>
                <Button leftIcon={<FaArrowLeft />} onClick={() => {
                    updateDevices(undefined)
                    setCurrDevice(undefined)
                }}>Back</Button>
            </Flex>

            <Device deviceId={currDevice} />
        </>



    if (!deviceList)
        return <Spinner />

    const deviceComps = Object.entries(deviceList).map(([deviceId, { device }]) => {
        const dev = device.DEVICE
        let devIcon = <></>
        const style = {
            width: "2.5em",
            height: "2.5em"
        }

        switch (dev) {
            case "pi":
                devIcon = <FaRaspberryPi style={style} />
                break;
            case "esp8266":
                devIcon = <FaMicrochip style={style} />
                break
            default:
                break;
        }
        return <Button
            flexDirection='column'
            w='10em'
            h='10em'
            alignItems='center'
            justifyContent='space-evenly'
            key={`${dev}-DeviceList`}
            onClick={() => {
                setCurrDevice(deviceId)
                updateDevices(deviceId)
            }}
        >
            {devIcon}
            <Text>{deviceId}</Text>
        </Button>
    })

    return <>
        <Flex
            justifyContent='center'
            alignItems='center'
            flexDir='column'
            mt='4'
            mb='6'
            gap='2'
            w='100%'
            h='100%'
        >
            {baseElements}
            <Heading>Devices</Heading>
            <ToggleEverything deviceList={deviceList} setUpdate={setUpdate}/>
            <Flex
            gap='3'
            w='100%'
            justifyContent='center'
            >
                {deviceComps}
            </Flex>
        </Flex>
    </>
}

export default App