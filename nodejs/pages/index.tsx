import type { NextPage } from 'next'
import Head from 'next/head'
import { Box } from "@chakra-ui/react"
import { useEffect, useState } from 'react'
import { AvailableData } from '../components/interface'

const Home: NextPage = () => {
  const [ available, setAvailable] = useState<AvailableData | undefined>(undefined)

  useEffect(() => {
    const { protocol, host } = location
    const url = `${protocol}//${/*host*/"10.6.0.1:6789"}/available`
    
    fetch(url)
      .then(e => e.json())
      .then(e => setAvailable(e))
  }, [])

  return (
    <Box>
        <Head>
          <title>Control LED Visualizer</title>
        </Head>
    </Box>
  )
}

export default Home
