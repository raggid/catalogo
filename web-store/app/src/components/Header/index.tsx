import { useContext, useRef } from 'react'
import { SearchContext } from '../../contexts/SearchContext'
import { api } from '../../services/api'
import styles from './styles.module.scss'
import Image from 'next/image'

export function Header() {
  const { searchString, updateSearch } = useContext(SearchContext)
  const { products, updateProducts } = useContext(SearchContext)

  const inputRef = useRef<HTMLInputElement>(null);

  function setSearchString() {
    updateSearch(inputRef.current.value)
  }

  return (
    <header className={styles.container}>
      <Image width={124} height={124} src="/logo.png" alt="Norte Auto Peças" objectFit='cover' />
      <input type="text" ref={inputRef} onSubmit={() => setSearchString()}></input>
      <button type="button" onClick={() => setSearchString()}>Buscar</button>

    </header>
  )
}



