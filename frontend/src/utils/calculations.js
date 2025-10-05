export function probability(count, total){
  if (!total) return 0
  return (100 * count / total)
}
