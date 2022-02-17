import { Flex } from '@chakra-ui/react'
import ReactGPlayer from "react-gcolor-picker"
import { VarProps } from '../interface'
import { hexToRgb, rgbToHex } from '../tools'


const linearMatcher = /linear-gradient\(90deg,(\s*(#[0-9a-fA-F]{6}\s*\d{1,3}\.*\d{0,2}%),*)+\);*/g
const defaultGrad = "linear-gradient(90deg, #ffffff 0.00%, #ff0000 100.00%);"

export default function GradientComponent({ curr, onChange}: VarProps<GradientOut>) {
    const onCompChange = (e: string) => {
        const matches = e.match(linearMatcher)?.length !== 0
        if(!matches)
            return onChange(cssToGradient(defaultGrad) as GradientOut)

        return onChange(cssToGradient(e) as GradientOut)
    }

    return <Flex w='100%' justifyContent='center' alignItems='center'>
        <ReactGPlayer
        solid={false}
        gradient={true}
        showAlpha={false}
        showGradientAngle={false}
        showGradientPosition={false}
        showGradientMode={false}

        value={curr ? gradientToCss(curr) : defaultGrad}
        onChange={e => onCompChange(e)} format={"hex"}
    />
    </Flex>
}

export function gradientToCss(grad: GradientOut) {
    const comps = grad.map(( [step, rgb] ) => {
        const [ r, g, b ] = rgb
        const percent = (step * 100).toFixed(2) + "%"

        const hex = rgbToHex(r, g, b)

        return `${hex} ${percent}`
    })

    return `linear-gradient(90deg, ${comps.join(", ")});`
}

const valueMatcher = /(\s*(#[0-9a-fA-F]{6}\s*\d{1,3}\.*\d{0,2}%))(?=\);)*/g
const hexMatcher = /#[0-9a-fA-F]{6}/g
const percentMatcher = /\d{1,3}\.*\d{0,2}%/g

export function cssToGradient(css: string) {
    const isValid = css.match(linearMatcher)?.length !== 0
    if(!isValid) {
        console.error("Invalid gradient", css)
        return null
    }

    const matches = css.match(valueMatcher)
    if(!matches)
        return null

    const mapped = matches.map(e => {
        const hex = e.match(hexMatcher)?.[0]
        const percent = e.match(percentMatcher)?.[0]?.replace("%", "")

        if (!hex || !percent)
            return null

        const rgb = hexToRgb(hex)
        if (!rgb)
            return null

        const step = parseFloat(percent) / 100
        return [step, rgb]
    })
    .filter(e => {
        if(!e)
            return false

        return true
    }) as GradientOut


    return mapped
}

export type GradientOut = [ Step, [ number, number, number ]][]
export type Step = number