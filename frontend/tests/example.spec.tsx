import { render } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Button from '../src/components/ui/Button'

describe('Button', () => {
  it('renders text', () => {
    const { getByText } = render(<Button>Hi</Button>)
    expect(getByText('Hi')).toBeDefined()
  })
})
