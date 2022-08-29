declare module "cytoscape-cose-bilkent" {
  import cy from "cytoscape"
  const coseBilkent: cy.Ext

  export interface LayoutOptions extends cy.LayoutOptions {
    name: "cose-bilkent"
    // Called on `layoutready`
    ready: () => void
    // Called on `layoutstop`
    stop: () => void
    // 'draft', 'default' or 'proof"
    // - 'draft' fast cooling rate
    // - 'default' moderate cooling rate
    // - "proof" slow cooling rate
    quality: "default" | "draft" | "proof"
    // Whether to include labels in node dimensions. Useful for avoiding label overlap
    nodeDimensionsIncludeLabels: boolean
    // number of ticks per frame; higher is faster but more jerky
    refresh: number
    // Whether to fit the network view after when done
    fit: boolean
    // Padding on fit
    padding: number
    // Whether to enable incremental mode
    randomize: boolean
    // Node repulsion (non overlapping) multiplier
    nodeRepulsion: number
    // Ideal (intra-graph) edge length
    idealEdgeLength: number
    // Divisor to compute edge forces
    edgeElasticity: number
    // Nesting factor (multiplier) to compute ideal edge length for inter-graph edges
    nestingFactor: number
    // Gravity force (constant)
    gravity: number
    // Maximum number of iterations to perform
    numIter: number
    // Whether to tile disconnected nodes
    tile: boolean
    // Type of layout animation. The option set is {'during', 'end', false}
    animate: "during" | "end" | false
    // Duration for animate:end
    animationDuration: number
    // Amount of vertical space to put between degree zero nodes during tiling (can also be a function)
    tilingPaddingVertical: number
    // Amount of horizontal space to put between degree zero nodes during tiling (can also be a function)
    tilingPaddingHorizontal: number
    // Gravity range (constant) for compounds
    gravityRangeCompound: number
    // Gravity force (constant) for compounds
    gravityCompound: number
    // Gravity range (constant)
    gravityRange: number
    // Initial cooling factor for incremental layout
    initialEnergyOnIncremental: number
  }

  export default coseBilkent
}
