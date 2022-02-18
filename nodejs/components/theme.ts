import { ComponentStyleConfig, extendTheme, ThemeConfig } from '@chakra-ui/react';

const switchComp: ComponentStyleConfig = {
    variants: {
        'blue': (props) => ({
            bgColor: 'black'
        })
    }
}

const config: ThemeConfig = {
    initialColorMode: "dark",
    useSystemColorMode: false
}

const theme = extendTheme({
    config
})

export default theme