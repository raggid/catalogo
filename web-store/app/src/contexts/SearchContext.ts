import { createContext } from "react"

type Product = {
  id: string
  code: string,
  provider: string,
  description: string,
  techSpecs: [],
  applications: []
}

type SearchContextData = {
  searchString: string
  updateSearch: (text: string) => void
  products: Product[]
  updateProducts: (products: Product[]) => void
}

export const SearchContext = createContext({} as SearchContextData)