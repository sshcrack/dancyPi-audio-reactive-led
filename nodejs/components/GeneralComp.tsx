import { Box, Flex, Heading } from '@chakra-ui/react'
import { General, StoredData } from "./interface"
import { ComponentTypes, typeComponents } from './types/components'
import styles from "../styles/generalComp.module.css"

export default function GeneralComp({ data: mode, onStoredChange, stored }: CompProps) {
    const { name: outerName, vars } = mode
    const varComps = vars.map(e => {
        const { name, type } = e
        const loc = `${outerName}_${name}`

        if (!Object.keys(typeComponents).includes(type))
            return <p>Type {type} not found</p>

        const Comp = typeComponents[type as ComponentTypes]
        if (!Comp)
            return <p>Type {type} not found</p>


        const onChange = (val: unknown) => {
            stored[loc] = val
            onStoredChange(stored)
        }

        const curr = stored[loc]

        return <>
            <Flex key={`flex-${loc}`} w='100%' className={styles.comp} justifyContent='center' alignItems='center'>
                <Flex flex='.4' justifyContent='center' alignItems='center'>
                    <p>{name}</p>
                </Flex>
                <Box className={styles.compContainer}>
                    <Comp variable={e} key={`${loc}-comp`} onChange={onChange} curr={curr} />
                </Box>
            </Flex>
            <Box mt='1em' key={`spacer-${loc}`}></Box>
        </>
    })

    return <Flex flexDir='column' w='100%' alignItems='center' justifyContent='center'>
        <Box mt='2em' />
        {varComps}
    </Flex>
}

interface CompProps {
    data: General,
    onStoredChange: (data: StoredData) => void
    stored: StoredData
}