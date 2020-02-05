/// Some documentation with math: $S = \\{ x \in \mathbb{N} \mid x \geq 42 \\}$.
pub fn is_more_than_universe(x: i32) -> bool {
    return x >= 42;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_more_than_nine() {
        assert!(is_more_than_universe(42));
        assert!(is_more_than_universe(2345));
        assert!(!is_more_than_universe(4));
        assert!(!is_more_than_universe(-10));
    }
}
