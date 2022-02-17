import { Box, Flex, Heading, Select, Spinner, useToast } from "@chakra-ui/react"
import type { NextPage } from 'next'
import Head from 'next/head'
import { useCallback, useEffect, useState } from 'react'
import { FaRaspberryPi } from "react-icons/fa"
import GeneralComp from '../components/GeneralComp'
import { AvailableData, General, NormalStorageKeys, StoredData } from '../components/interface'
import { capitalizeWord } from '../components/tools'
import styles from "../styles/index.module.css"

const Home: NextPage = () => {
  const [available, setAvailable] = useState<AvailableData | undefined>(undefined)
  const [storage, setStorage] = useState<StoredData | undefined>(undefined)
  const [update, setUpdate] = useState<number>(0);
  const updateStorage = useCallback((key: keyof NormalStorageKeys, value: string) => {
    if (!storage)
      return

    //@ts-ignore dunno why it is doing like dis
    storage[key] = value
    setStorage({ ...storage})
  }, [ setStorage, storage ])

  const toast = useToast()

  useEffect(() => {
    const { protocol, host } = location
    const base = `${protocol}//${/*host*/"10.6.0.1:6789"}`

    const availableUrl = `${base}/available`
    const varsUrl = `${base}/vars`

    const fetchProm = (url: string) => {
      return fetch(url)
        .then(e => e.json())
    }

    const allProms = [ fetchProm(availableUrl), fetchProm(varsUrl)]
    Promise.all(allProms)
      .then(([ available, storage]) => {
        setAvailable(available)
        setStorage({ ...storage})
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [update, setUpdate])
  const { modes, filters } = available ?? {}


  const modeSelector = getSelector("mode", modes, storage, mode => updateStorage("mode", mode))
  const filterSelector = getSelector("filter_mode", filters, storage, filter => updateStorage("filter_mode", filter))

  const currMode = modes && storage ? modes?.find(e => e.name === storage.mode) : undefined
  const currFilter = filters && storage ? filters?.find(e => e.name === storage.filter_mode) : undefined


  const onStoreChange = (newData: StoredData) => setStorage({ ...newData })

  const modeSettings = currMode && storage ? <GeneralComp data={currMode} stored={storage} onStoredChange={onStoreChange} /> : <Spinner />
  const filterSettings = currFilter && storage ? <GeneralComp data={currFilter} stored={storage} onStoredChange={onStoreChange} /> : <Spinner />
  return (
    <>
      <Head>
        <title>Control LED Visualizer</title>
      </Head>
      <Flex justifyContent='center' alignItems='center' flexDirection='column'>
        <Flex justifyContent='center' alignItems='center'>
          <FaRaspberryPi style={{width: '30%', height: '30%'}} />
          <Heading>Raspberry PI Visualizer</Heading>
        </Flex>

        <Box mt='3em' />

        <Heading>Effect</Heading>
        <Box mt='1em' />
        <Flex className={styles.generalBox} justifyContent='center' alignItems='center' flexDir='column'>
          {modeSelector}
          {modeSettings}
        </Flex>

        <Box mt='3em' />

        <Heading>Filter</Heading>
        <Box mt='1em' />
        <Flex className={styles.generalBox} justifyContent='center' alignItems='center' flexDir='column'>
          {filterSelector}
          {filterSettings}
        </Flex>
      </Flex>
    </>
  )
}

function getSelector(default_key: string, data: General[] | undefined, storage: StoredData | undefined, onChange: ChangeFunc) {
  const keys = data?.map(e => e.name) ?? []

  return <Box className={styles.selector}>
    {!data || !storage ?
    <Spinner /> :
    <Select defaultValue={storage[default_key]} onChange={e => {
      if(!e?.target?.value)
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

type ChangeFunc = (newMode: string) => void

export default Home
