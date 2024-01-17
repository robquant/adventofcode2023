use std::collections::HashSet;

#[derive(Debug)]
#[allow(dead_code)]
struct Card {
    id: i32,
    winning_numbers: HashSet<i32>,
    my_numbers: HashSet<i32>,
}

fn parse_line(line: &str) -> Card {
    let parts: Vec<&str> = line.split(':').collect();
    let id = parts[0]
        .trim_start_matches("Card")
        .trim()
        .parse::<i32>()
        .unwrap();
    let sets: Vec<&str> = parts[1].split('|').collect();
    let mut my_numbers: HashSet<i32> = HashSet::new();
    let mut winning_numbers: HashSet<i32> = HashSet::new();

    if let Some(first_part) = sets.get(0) {
        winning_numbers = first_part
            .split_whitespace()
            .filter_map(|num| num.parse().ok())
            .collect();
    }

    if let Some(second_part) = sets.get(1) {
        my_numbers = second_part
            .split_whitespace()
            .filter_map(|num| num.parse().ok())
            .collect();
    }

    Card {
        id,
        winning_numbers,
        my_numbers,
    }
}

fn score(card: &Card) -> u64 {
    let common_elements = card.winning_numbers.intersection(&card.my_numbers).count() as u32;
    if common_elements > 0 {
        2u64.pow(common_elements - 1)
    } else {
        0
    }
}

fn part1(cards: &Vec<Card>) -> u64 {
    cards.iter().map(|card| score(card)).sum()
}

fn part2(cards: &Vec<Card>) -> u64 {
    // Initially we have 1 of each card
    let mut counts = vec![1; cards.len()];
    // !!! NOT vec![1, cards.len()]
    // let mut counts = Vec::new();
    // counts.resize(cards.len(), 1);

    for (i, card) in cards.iter().enumerate() {
        let card_score = card.winning_numbers.intersection(&card.my_numbers).count();
        for j in 1..=card_score {
            counts[i + j] += counts[i];
        }
    }
    counts.iter().sum()
}
fn main() {
    let mut cards: Vec<Card> = Vec::new();

    for line in std::io::stdin().lines() {
        let card = parse_line(&line.unwrap());
        cards.push(card);
    }

    println!("Part 1: {}", part1(&cards));
    println!("Part 2: {}", part2(&cards));
}
