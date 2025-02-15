import { Box, Button, Flex, Heading, IconButton, Select, Spinner, Switch, Text, useToast } from "@chakra-ui/react"
import { ChangeEvent, Dispatch, useCallback, useEffect, useState } from 'react'
import { FaLock, FaUnlock } from "react-icons/fa"
import './App.css'
import EnergyComp from './components/Energy'
import GeneralComp from './components/GeneralComp'
import { AvailableData, General, NormalStorageKeys, StoredData, Var } from './components/interface'
import { capitalizeWord, getBaseUrl } from './components/tools'

function Device({ deviceId }: { deviceId: string }) {
  const [available, setAvailable] = useState<AvailableData | undefined>(undefined)
  const [stored, setStorage] = useState<StoredData | undefined>(undefined)
  const [isLoading, setLoading] = useState(true)
  const [update, setUpdate] = useState<number>(0);
  const [isSaving, setSaving] = useState(false);
  const toast = useToast()
  const updateStorage = useCallback((key: keyof NormalStorageKeys, value: string) => {
    if (!stored)
      return

    //@ts-ignore dunno why it is doing like dis
    stored[key] = value
    setStorage({ ...stored })
  }, [setStorage, stored])
  const save = useCallback(() => {
    if (!isSaving)
      setSaving(true)
    saveOuter(available, stored, toast, isSaving, setSaving, deviceId)
      .finally(() => {
        setSaving(false)
      })
  }, [stored, isSaving, toast, available, deviceId])


  useEffect(() => {
    setLoading(true)
    const base = getBaseUrl(window.location)

    const availableUrl = `${base}/available?device_id=${deviceId}`
    const varsUrl = `${base}/vars?device_id=${deviceId}`

    const fetchProm = (url: string) => {
      return fetch(url)
        .then(e => e.json())
    }

    const allProms = [fetchProm(availableUrl), fetchProm(varsUrl)]
    Promise.all(allProms)
      .then(([available, storage]) => {
        setAvailable(available)
        setStorage({ ...storage })
      })
      .catch(e => {
        toast({
          title: "Error",
          description: `Could not fetch data from ${base}. Retrying...`,
          status: "error",
        })
        console.error(e)

        setTimeout(() => {
          setUpdate(Math.random())
        }, 1000)
      })
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [update, setUpdate])
  const { modes, filters } = available ?? {}


  const modeSelector = getSelector("mode", modes, stored, mode => updateStorage("mode", mode))
  const filterSelector = getSelector("filter_mode", filters, stored, filter => updateStorage("filter_mode", filter))

  const currMode = modes && stored ? modes?.find(e => e.name === stored.mode) : undefined
  const currFilter = filters && stored ? filters?.find(e => e.name === stored.filter_mode) : undefined


  const onStoreChange = (newData: StoredData) => setStorage({ ...newData })


  const modeSettings = currMode && stored ? <GeneralComp data={currMode} stored={stored} onStoredChange={onStoreChange} /> : <Spinner />
  const filterSettings = currFilter && stored ? <GeneralComp data={currFilter} stored={stored} onStoredChange={onStoreChange} /> : <Spinner />

  const content = <>
    <Heading>Effect</Heading>
    <Box mt='1em' />
    <Flex className='generalBox' justifyContent='center' alignItems='center' flexDir='column'>
      {modeSelector}
      {modeSettings}
    </Flex>

    <Box mt='1.5em' />

    <Heading>Filter</Heading>
    <Box mt='1em' />
    <Flex className='generalBox' justifyContent='center' alignItems='center' flexDir='column'>
      {filterSelector}
      {filterSettings}
    </Flex>
    <Box mt='1.5em' />

    <Heading>General Visualization</Heading>
    <Box mt='1em' />

    <Flex className='generalBox' justifyContent='center' alignItems='center'>
      {
        stored ? <EnergyComp onChange={onStoreChange} stored={stored} /> : <Spinner />
      }
    </Flex>

    <Box mt='1.5em' />
    <Flex justifyContent='center' alignItems='center' gap='5rem' mr='1' ml='1' mb='4'>
      <Button colorScheme='green' w='15em' isLoading={isSaving} onClick={save}>
        Save Changes
      </Button>
      <Button colorScheme='red' w='15em' isLoading={isLoading} onClick={() => setUpdate(Math.random())}>
        Reset
      </Button>
    </Flex>
  </>

  const enabled = stored ? stored.enabled : false
  const locked = stored ? stored.locked : false
  const onSwitchEnable = async (e: ChangeEvent<HTMLInputElement>) => {
    if (!stored || stored.locked)
      return

    const checked = e.target.checked

    stored.enabled = checked
    setStorage({ ...stored })
    const base = getBaseUrl(window.location)

    const res = await fetch(`${base}/enabled?enabled=${checked}&device_id=${deviceId}`)
      .catch(e => { console.error(e) })

    const success = res && res?.status === 200
    if (success)
      return

    toast({
      title: "Error",
      status: "error",
      description: "Could not enable/disable led strips"
    })
    stored.enabled = !checked
    setStorage({ ...stored })
    setUpdate(Math.random())
  }

  const toggleLock = async () => {
    if (!stored)
      return

    const locked = !stored.locked

    stored.locked = locked
    setStorage({ ...stored })
    const base = getBaseUrl(window.location)

    const res = await fetch(`${base}/locked?locked=${locked}&device_id=${deviceId}`)
      .catch(e => { console.error(e) })

    const success = res && res?.status === 200
    if (success)
      return

    toast({
      title: "Error",
      status: "error",
      description: "Could not unlock led strips"
    })
    stored.locked = !locked
    setStorage({ ...stored })
    setUpdate(Math.random())
  }

  return (
    <>
      <Flex justifyContent='center' alignItems='center' flexDirection='column' mt='4'>
        <Flex justifyContent='space-around' className='topControl'>
          <Flex justifyContent='center' alignItems='center'>
            <Switch mr='2rem' size='lg' isChecked={enabled} onChange={e => onSwitchEnable(e)} disabled={locked} />
            <Text>{enabled ? "turned On" : "turned Off"}</Text>
          </Flex>
          <Flex justifyContent='center' alignItems='center'>
            <IconButton icon={locked ? <FaLock /> : <FaUnlock />} onClick={() => toggleLock()} aria-label="Lock/Unlock gesture" />
          </Flex>
        </Flex>
        <Box mt='2em' />

        {!stored ? <Spinner /> : enabled ? content : <></>}
      </Flex>
    </>
  )
}


function getSelector(default_key: string, data: General[] | undefined, storage: StoredData | undefined, onChange: ChangeFunc) {
  const keys = data?.map(e => e.name) ?? []

  return <Box className='selector'>
    {!data || !storage ?
      <Spinner /> :
      <Select defaultValue={storage[default_key]} onChange={e => {
        if (!e?.target?.value)
          return

        onChange(e.target.value)
      }}>
        {keys.map(e =>
          <option
            key={e}
            value={e}
          >
            {capitalizeWord(e)}
          </option>
        )}
      </Select>}
  </Box>
}

async function saveOuter(available: AvailableData | undefined, stored: StoredData | undefined, toast: Toast, isSaving: boolean, setSaving: Dispatch<boolean>, deviceId: string) {
  if (isSaving)
    return

  if (!stored || !available)
    return toast({
      title: "Error",
      description: "Data hasn't been loaded yet. Can't save",
      status: "error"
    })

  const strMode = stored.mode
  const strFilter = stored.filter_mode

  const currMode = available.modes.find(e => e.name === strMode)
  const currFilter = available.filters.find(e => e.name === strFilter)
  if (!currMode)
    return toast({
      title: "Error",
      description: "Mode could not be found."
    })

  if (!currFilter)
    return toast({
      title: "Error",
      description: "Filter could not be found."
    })


  const modeQueries = getQueryParams(strMode, currMode.vars, stored)
  const filterQueries = getQueryParams(strFilter, currFilter.vars, stored)
  const energyQuery = getEnergyQuery(stored)

  const anyErrors = modeQueries.some(e => (!e && typeof e !== "boolean") || typeof e === "undefined") || filterQueries.some(e => !e)
  if (anyErrors) {
    console.error(filterQueries, modeQueries, stored, currMode, currFilter)
    return toast({
      title: "Error",
      description: "Some variables could not be obtained."
    })
  }

  const base = getBaseUrl(window.location);
  const modeQuery = (modeQueries as string[]).join("&")
  const filterQuery = (filterQueries as string[]).join("&")


  const proms = [
    fetch(`${base}/setmode?mode=${strMode}&${modeQuery}&device_id=${deviceId}`),
    fetch(`${base}/filter?mode=${strFilter}&${filterQuery}&device_id=${deviceId}`),
    fetch(`${base}/energy?${energyQuery}&device_id=${deviceId}`)
  ]

  const onError = (e: unknown) => {
    console.error(e)
    toast({
      title: "Error",
      status: "error",
      description: "Could not save data. Look at console for more info.",
    })
  }

  const onSuccess = () => {
    toast({
      title: "Saved",
      status: "success"
    })
  }

  return Promise.all(proms)
    .then(res => {
      if (res.some(e => e.status !== 200))
        return onError(res)

      onSuccess()
    })
    .catch(e => onError(e))
}

function getQueryParams(prefix: string, vars: Var[], stored: StoredData) {
  console.log("Query Params")
  return vars.map(({ name }) => {
    const storedKey = `${prefix}_${name}`
    let value = stored[storedKey]

    console.log(storedKey, value)
    if (typeof value === "undefined" || typeof name === "undefined")
      return undefined

    if (typeof value === "object")
      value = JSON.stringify(value)

    return `${encodeURIComponent(name)}=${encodeURIComponent(value)}`
  })
}

function getEnergyQuery(stored: StoredData) {
  const brightness = stored.energy_brightness
  const brightnessMult = stored.energy_brightness_mult

  const speed = stored.energy_speed
  const speedMult = stored.energy_speed_mult

  const sensitivity = stored.energy_sensitivity

  return `brightness=${brightness}&brightness_mult=${brightnessMult}&speed=${speed}&speed_mult=${speedMult}&sensitivity=${sensitivity}`
}

type ChangeFunc = (newMode: string) => void
type Toast = ReturnType<typeof useToast>


export default Device;
