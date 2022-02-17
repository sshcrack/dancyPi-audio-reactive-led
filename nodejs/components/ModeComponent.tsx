import { Mode } from "./interface"

export default function ModeComponent(mode: Mode) {
    const { name } = mode
    
    return <h1>{name}</h1>
}