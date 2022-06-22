#QUERIES FOR KITSU GRAPHQL API

BASE_URL = "https://kitsu.io/api/graphql"

# ================ ANIME ================

ANIME_BY_ID: str = """
            query animeByID($id: ID!) {
                findAnimeById(id: $id) {
                    id
                    slug
                    createdAt
                    updatedAt
                    startDate
                    endDate
                    description
                    status
                    sfw
                    subtype
                    ageRating
                    endDate
                    season
                    episodeCount
                    episodeLength
                    totalLength
                    youtubeTrailerVideoId
                    averageRatingRank
                    averageRating
                    userCountRank
                    titles{
                        canonical
                        localized
                    }
                    posterImage {
                        original {
                            url
                        }
                        views {
                            name
                            url
                        }
                    }
                    bannerImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }      
                    }
                }
            }
"""

ANIME_BY_ID_EPISODES: str = """
            query episodes ($id: ID!, $limit: Int!) {
                findAnimeById(id: $id) {
                episodes (first: $limit) {
                nodes {
                    id
                    length
                    number
                    titles {
                        canonical
                        localized
                    }
                    description
                    thumbnail {
                        original {
                            url
                        }
                    }
                    }
                }
                }
            } 
"""

ANIME_BY_ID_REVIEWS: str = """
            query reviews ($id: ID!, $limit: Int!) {
                findAnimeById(id: $id) {
                reactions (first: $limit) {
                nodes {
                    id
                    progress
                    reaction
                }
                }
                }
            }
"""

ANIME_BY_ID_CHARACTERS: str = """
            query characters ($id: ID!) {
                findAnimeById(id: $id) {
                characters (first: 100) {
                nodes {
                    role
                    character {
                    createdAt
                    updatedAt
                    id
                    slug
                    description
                    names {
                        canonical
                        localized
                    }
                    image {
                        original {
                        url
                        }
                        views {
                        url
                        }
                    }
                    }
                }
                }
                }
            }
"""

ANIME_BY_ID_CATEGORIES: str = """
            query category ($id: ID!) {
                findAnimeById(id: $id) {
                categories (first: 25) {
                nodes {
                    title
                    slug
                    description
                    isNsfw
                }
                }
                }
            }
"""

ANIME_BY_ID_STREAMLINKS: str =  """
            query streamLinks ($id: ID!) {
                findAnimeById(id: $id) {
                streamingLinks (first: 10) {
                nodes {
                    id
                    streamer {
                        siteName
                    }
                    subs
                    dubs
                    url
                } 
                }
                }
            }
"""

# ================ MANGA ================

MANGA_BY_ID: str = """
        query animeByID ($id: ID!) {
        findMangaById(id: $id) {
            id
            slug
            createdAt
            updatedAt
            startDate
            endDate
            description
            status
            sfw
            subtype
            ageRating
            endDate
            chapterCount
            volumeCount
            averageRatingRank
            averageRating
            userCountRank
            titles{
            canonical
            localized
            }
            posterImage {
            original {
                url
            }
            views {
                name
                url
            }
            }
            bannerImage {
            original {
                url
            }
            views {
                name
                url
            }      
            }
        }

        }
"""

MANGA_BY_ID_CHAPTERS = """
query chapters ($id: ID!, $limit: Int) {
  findMangaById(id: $id) {
    chapters (first: $limit) {
      nodes {
        id
        createdAt
        updatedAt
        titles {
          romanized
        }

        description
        number
        thumbnail {
          original {
            url
        }
    }
    }
    }
  }
}
"""
# ================ USERS ================

USERS_BY_ID: str = """
            query user ($id: ID!) {
            findProfileById (id: $id) {
                id
                name
                slug
                birthday 
                about
                location
                waifuOrHusbando
                gender
                proTier
                url
                posts (first: 1) {
                    totalCount
                }
                mediaReactions(first: 1){
                    totalCount
                }
                comments (first: 1) {
                    totalCount
                }
                followers (first: 1){
                    totalCount
                }
                following (first: 1){
                    totalCount
                }
                favorites (first: 1){
                    totalCount
                }
                avatarImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }
                }
                bannerImage {
                    original {
                        url
                    }
                    views {
                        name
                        url
                    }
                }
            }
            }
"""

USERS_BY_ID_SOCIAL = """
            query user ($id: ID!) {
            findProfileById (id: $id) {
                siteLinks (first: 30) {
                nodes {
                    id
                    url
                }
                }
            }
            }
"""